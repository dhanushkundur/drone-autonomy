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
