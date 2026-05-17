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