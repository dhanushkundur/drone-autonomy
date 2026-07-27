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
- Set up MAVLink UDP output in Mission Planner (Ctrl+F -> MAVLink -> UDP Outbound port 14550)
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

## Late May / June 2026 - Transition from sim to hardware
Decided to stop living in simulation and commit to a real airframe. Renamed the
project ATLAS (Autonomous Tracking and Landing Aerial System) and reframed the
whole thing around a flight-first build strategy: get a stable manual hover on
real hardware before adding any autonomy or vision. Sim work (pymavlink mission
scripts, OpenCV tracking prototype) stays as a foundation but is no longer the
critical path.

Hardware selected and locked:
- FC: Corvon H743 (CORVON743V1 in ArduPilot), running ArduCopter 4.8.0-dev
- ESC: Corvon 50A 4-in-1, BLHeli_S / Bluejay, DShot300
- Motors: Emax ECO II 2207 2400KV, 4S
- Props: HQProp 5x4.3x3 V2S tri-blade
- TX: BetaFPV LiteRadio 3 (ELRS). RX: RadioMaster RP3 Diversity 2.4GHz ELRS
- Battery: Zeee 4S 1500mAh
- Frame: custom single-piece PETG center frame, plus configuration, carbon tube arms
- GPS (Phase 2): Corvon M10
- Companion computer (deferred to Phase 3): Raspberry Pi 5

Key learnings:
- Verify every CAD dimension from datasheets or physical measurement, not memory.
  The Emax mount pattern is 16x16mm M3, confirmed by measurement after an initial
  wrong assumption cost a reprint.
- PETG is the right material for a learning/demonstrator airframe: tougher than PLA,
  no enclosure needed. Not the strongest option, but appropriate here.
- Round carbon tubes with set-screw motor mounts can rotate under torque. Nylon-tip
  set screws and keying the tube help. This bit me later (see below).

## June 2026 - Frame build and bench configuration
- Designed and printed the single-piece PETG center frame on a Bambu Lab A1 (SUNLU PETG)
- Cut carbon tube arms, dry-fit and set final geometry (~108mm center-to-shaft,
  ~26mm tip-to-tip prop clearance on 5-inch props)
- Assembled FC/ESC stack on grommets, mounted in frame
- Flashed ArduPilot via STM32CubeProgrammer (DFU), set frame params
- 6-position accel calibration
- Set AHRS_ORIENTATION=2 (Yaw90) to resolve an apparent pitch/roll axis swap seen
  during accel cal. NOTE: this fix was validated by feel and a glance at the HUD,
  not by a tilt test. This turned out to be incomplete and caused the first-hover
  flip weeks later (see July 27).
- Enabled battery monitor (BATT_MONITOR=4, BATT_VOLT_PIN=10, BATT_CURR_PIN=11)

## Early July 2026 - Soldering, RC link, failsafe
- Completed all ESC/motor soldering, XT60 leads, capacitor
- Discovered DShot600 is incompatible with the Bluejay ESC on this hardware.
  Switched to DShot300 (MOT_PWM_TYPE=5), which immediately produced motor response.
  Confirmed with the ESC manufacturer.
- Motor order was scrambled; corrected via SERVO_FUNCTION remap
  (SERVO1=36, SERVO2=34, SERVO3=33, SERVO4=35)
- Left motor direction had to be reversed directly in esc-configurator.com because
  Bluejay ignored SERVO_BLH_RVMASK on that channel. NOTE: this setting lives on the
  ESC chip, not in the .param file, so it is invisible to param backups.
- Fixed a persistent "RC not found" fault: yellow/green data wires in the RX pigtail
  were effectively swapped at the FC end. Fix was a deliberate non-standard swap at
  the RP3 pad (green on T, yellow on R). By design, not an error.
- Failsafe: FS_THR_ENABLE=1, relying on CRSF protocol-level link-loss detection,
  because the RP3 holds last channel values on signal loss (throttle threshold alone
  is insufficient). Bench-tested with TX off: FC declares failsafe and disarms.

Key learnings:
- Hand-held throttle testing with props on is dangerous and produces unreliable data.
  Instrument data (telemetry logs, Mission Planner) is ground truth, not feel.
- Battery sag across long bench sessions is a major confounding variable. A sagging
  pack produced apparent motor imbalance and instability that was entirely battery-induced.

## July 27, 2026 - FIRST STABLE HOVER (and the flip that hid for weeks)
The aircraft flew. First stable manual hover achieved. Phase 1 complete.

This session was a long debugging arc that ended by finding the true cause of the
first-hover flip, which had survived every previous component check.

Getting to an armable state:
- Onboard logging: 128GB and an old 8GB microSD both failed with "PreArm: Logging
  failed" (128GB forced to FAT32 fails ArduPilot's SD driver; 8GB was dead). A new
  SanDisk Ultra 32GB, formatted FAT32, fixed it on the first try. LOG_BACKEND_TYPE=1.
  Lesson: 32GB or smaller, native FAT32. Don't fight oversized cards.
- Voltage read 0.03V after the SD reseat, blocking arm. Cause: I knocked the ESC->FC
  voltage-sense pin loose while seating the card. Reseated it and voltage read correct.
  A parameter can scale a voltage reading, but it cannot make a connected sense line
  read ~0V. Near-zero = no signal = physical, not a parameter.
- BATT_ARM_VOLT had been left at 14.7 by the Initial Parameters wizard, too high.
  Set to 14.0.

Finding the flip cause:
- On carpet, both hands-off attempts flipped instantly on throttle-up. Logs showed
  ATT.Roll running to ~179 and ATT.Pitch swinging -50 to +35 while DesRoll/DesPitch
  stayed at zero. The FC commanded no attitude change; the aircraft diverged anyway.
  That is a real divergence, not a tune problem.
- Motors, props, spin directions, and mixing all checked out repeatedly. RCOU showed
  the FC driving the correct corners for the correction it was attempting. So the
  fault was upstream of the motors: the FC's sense of attitude.
- The definitive test was a static tilt check on the bench (disarmed, watching the HUD):
  pitching the nose UP showed GROUND, rolling RIGHT banked LEFT. Both attitude axes
  were inverted. Both axes inverted (without being crossed) = a 180-degree yaw error
  in AHRS_ORIENTATION.
- Root cause: AHRS_ORIENTATION was 2 (Yaw90) but should have been 6 (Yaw270). The
  original June fix uncrossed the axes (so pitch read as pitch, roll as roll) but left
  both inverted, which a level HUD cannot reveal. An inverted axis flips the sign of
  the stabilize feedback loop from negative (self-correcting) to positive (runaway),
  so the aircraft flips on every takeoff the instant the loop gains authority. Idle
  looks fine because the loop has no authority at zero throttle.
- Fix: set AHRS_ORIENTATION=6. Re-ran the tilt test: all four directions now track
  correctly. Re-ran Calibrate Level under the corrected orientation.

Result: first hover was rock stable, zero oscillation. The "wiggle" chased for weeks
was largely the FC fighting its own inverted feedback, and it disappeared once the
orientation was correct. Aircraft drifted slowly in one direction, which is expected
in Stabilize (attitude hold only, no position hold). Position drift is what GPS/Loiter
solves in Phase 2.

Key learnings:
- Verify AHRS_ORIENTATION with a tilt test that moves the aircraft through pitch and
  roll in both directions, not by feel or a level-HUD glance. A level HUD looks
  identical whether an axis is inverted or not; only tilting reveals the sign.
- An inverted attitude axis is a positive-feedback fault: perfect motors and props
  will still flip on every takeoff, and no motor/prop/mixing test can catch it.
- Instrumentation is what closed this. Weeks of hand tests could not; one logged flight
  plus a tilt check did. Get the data, read the data.
- First hover belongs on flat ground or grass, never carpet. Carpet grabs props and
  turns a small tip into a full tumble, contaminating the log.

Next session (Phase 2 - GPS autonomy):
- Install and configure Corvon M10 GPS, compass calibration
- BATT_VOLT_MULT calibration against a multimeter, then set proper failsafe thresholds
  (BATT_LOW_VOLT ~14.0, BATT_CRT_VOLT ~13.2)
- PID tuning / Autotune for the actual airframe
- Loiter, Position Hold, waypoint missions, RTL
