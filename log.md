# Project Log

## Day 1 - May 13, 2026
Setup and first flights.

What I did:
- Installed Mission Planner on Windows
- Launched ArduPilot SITL multirotor simulator
- First autonomous takeoff via Actions tab (arm, then right-click takeoff to 10m)
- Used Guided mode "Fly to Here" to send drone to a custom point on map
- Built a 4-waypoint mission in the PLAN screen
- Wrote mission to drone, set Auto mode, drone flew the entire mission autonomously

Key learnings:
- ArduPilot requires manual arm before any takeoff command works (safety feature)
- Guided mode = wait for commands. Auto mode = execute uploaded mission.
- The PLAN screen "Insert WP" dialog is just confirming insertion order, not an error.
- Home location is the takeoff/landing reference. Altitudes are relative to it.

Next session:
- Stop using the GUI buttons. Start writing Python scripts that send the same commands via MAVLink.
- Install Python and pymavlink.
- Write first script: connect to SITL, arm, takeoff to 10m, land. Programmatically.

## Day 2 - May 14, 2026
First Python script that talks to the drone.
- Set up MAVLink UDP output in Mission Planner (Ctrl+F → MAVLink → UDP Outbound port 14550)
- Wrote 01_connect.py: connects via pymavlink, waits for heartbeat, reads SYS_STATUS message, prints battery voltage
- Debugged port conflicts and connection refused errors
- Set up Git locally and linked to GitHub repo

Key learnings:
- Only one program can hold a port at a time
- TCP is reliable but slower, UDP is fast but messages can drop
- Port 5760 = SITL TCP default. 14550 = standard MAVLink UDP.
- recv_match(type='X', blocking=True) is the basic pattern for grabbing telemetry
- Drone messages have fields you access with msg.fieldname
- voltage_battery is in millivolts, not volts

## Day 3 - May 16, 2026
- Set up WSL with Ubuntu 22.04
- Built ArduPilot SITL from source
- Got 02_arm.py working: arms, takes off to 10m, reads altitude back
- Switched to VS Code with WSL extension for cleaner dev environment

## Phase 1 wrap-up - late May 2026
Refactored from loose scripts into a real API.
- Built the `Drone` class in `drone.py`: connect, arm, takeoff, fly_to, land, return_to_launch
- `main.py` now drives a full mission in six lines
- `fly_to` uses `set_position_target_global_int_send` with the velocity/yaw mask
- Wrote `distance_meters` as a flat-earth approximation (good enough for sub-km waypoints, would need haversine for longer)
- `return_to_launch` has a "low altitude held for 5 seconds" check before declaring landed, because motors_armed() goes false slightly after touchdown

Key learnings:
- A class makes the code reusable. The duplicate module-level functions are dead weight and need to be deleted.
- MAVLink's bitmask for position targets is the most confusing part of pymavlink. `0b0000111111111000` = use position, ignore velocity/accel/yaw.

## Computer vision pipeline - early June 2026
Built the perception side before touching hardware.
- `cv_detect.py`: HSV red-mask on a single image, biggest contour by area, bounding box, center coordinates
- `cv_video_detect.py`: same logic frame-by-frame on `test_video.mp4`
- `atlas_track.py`: closes the loop. Computes error_x from frame center, scales by YAW_GAIN, sends MAV_CMD_CONDITION_YAW relative commands to SITL

Key learnings:
- HSV is more robust than RGB for color thresholding under varying brightness
- `cv2.findContours` returns a list, always check length before max()
- Two real bugs in atlas_track.py I need to fix before hardware:
  1. Red mask only covers hue 0-10. Red wraps past 179, so I'm missing half the red spectrum.
  2. No deadzone in the yaw loop. When error_x is near zero the drone still gets tiny yaw commands and oscillates.

## Hardware selection - mid June 2026
Switched from "use a Pixhawk dev kit" to "design and build a custom 5-inch quad." Decision driven by: I want to actually understand the stack, not bolt one together from a kit.

Locked the build:
- FC: Corvon H743 (ArduPilot target `CORVON743V1`, 30.5x30.5mm mount)
- ESC: Corvon 50A 4-in-1 BLHeli_S, matched stack with the FC
- Motors: Emax ECO II 2207 2400KV, 4S. 16x16mm M3 bolt pattern.
- Battery: CNHL Black Series 4S 1500mAh 100C
- Radio: RadioMaster Pocket ELRS + BetaFPV ELRS Lite receiver
- Companion + camera (deferred until after manual hover): Raspberry Pi 5 4GB, Pi Camera Module 3 Wide
- GPS (deferred): Matek M10Q-5883

Strategy locked: **flight-first**. Get the thing hovering manually before any Pi, camera, or CV work. Adding autonomy to a drone that doesn't fly is just stacking unknowns.

Key learnings:
- Verify every spec from the datasheet, not from memory or from an LLM's first guess. I've already caught wrong dimensions (Pixhawk hole pattern when I should have been on the Corvon, wrong heat-set insert hole size) that would have caused reprints.
- Print-before-commit: print one motor mount, fit-test, then commit to printing four.

## Frame and CAD - mid to late June 2026
Designed in Onshape.
- 100x100mm octagonal dual-plate frame, 5mm PETG plates, 38mm gap
- Four 16mm OD carbon fiber tube arms, press-fit into plate sockets and motor mount sockets
- Motor mounts have a 4mm tall x 8mm diameter boss around the set screw hole for thread engagement
- Set screw hole sized to 4.0mm for 4.6mm OD M3 brass heat-set inserts (manufacturer-spec hole size)
- Bottom plate hole pattern updated from Pixhawk 32.1x28.5 to Corvon 30.5x30.5 at 3.2mm clearance
- Top plate: removed ESC mount holes (ESC now stacks with FC on bottom plate), kept Pi 5 holes, camera bracket holes, corner standoff holes

FC/ESC stack layout (locked):
- Bottom-up: M3 nut, bottom plate (3.2mm hole), ESC with soft-mount grommets, 8mm female-female nylon standoff, FC with grommets, M3 screw with washer
- Grommet measurements drove the 8mm standoff spec: 7mm total grommet height (1mm small flange, 1mm waist, 4mm large flange, plus board thickness)

Key learnings:
- An AI caught the set-screw crush risk on the carbon tube before I did. The boss + nylon-tipped set screw plus the proper insert hole size are the fix. I need to be the one catching these failure modes, not waiting to be told.
- "Don't relitigate locked decisions" applies to me too. Once a dimension is verified from source, stop second-guessing it.

## Hardware on order / arrived - late June 2026
Arrived:
- 16mm OD carbon fiber tubes, 500mm length, qty 2. Press-fit into motor mount socket is snug. Good.

On order:
- Emax ECO II 2207 motors
- M3 8mm female-female nylon standoffs
- M3x5x4.6mm brass heat-set inserts
- M3x8mm nylon-tip set screws

Blocked on motor arrival:
- Final motor mount reprint (need to verify wire clearance through the side slit before committing to four prints)
- Arm cut length (determined after motor mount fit test)
- Landing gear purchase (TPU feet, need to verify motor base M3 hole pattern matches)

## Current status - end of June 2026
Phase 3 in progress. Vision pipeline is functional in sim with two known bugs queued for fixing before hardware integration. Frame CAD is largely done. Motor mount reprint and arm assembly are the next physical milestones. First powered hover target: end of summer.

Next session priorities:
- Fix the two CV bugs (HSV wrap, yaw deadzone) or move them to KNOWN_ISSUES.md
- Delete duplicate module-level functions in drone.py
- Add requirements.txt and .gitignore
- When motors arrive: wire clearance check, reprint mounts, fit test, cut arms
