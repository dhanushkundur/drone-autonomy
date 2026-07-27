# ATLAS

**Autonomous Tracking and Landing Aerial System** — a custom-built 5-inch
quadcopter running ArduPilot, developed from simulation through to flying hardware.
The goal is a working autonomous aircraft: manual hover, then GPS-based autonomous
flight, then vision-guided target tracking.

**Status (July 27, 2026): First stable manual hover achieved. Phase 1 complete.**
Now moving into Phase 2 (GPS autonomy).

## Build strategy

Flight-first. The aircraft must achieve a stable, well-behaved manual hover before
any autonomy or vision code is added. Simulation work (pymavlink mission scripts,
OpenCV tracking prototype) is the software foundation, but hardware bring-up drives
the critical path.

## Phases

- **Phase 1 — Manual hover (COMPLETE):** Scratch-built airframe, ArduPilot config,
  RC link, failsafes, first stable hover in Stabilize.
- **Phase 2 — GPS autonomy (in progress):** Corvon M10 GPS, compass calibration,
  Position Hold / Loiter, waypoint missions, Return-to-Launch. Includes PID tuning
  / Autotune and battery-monitor calibration.
- **Phase 3 — Vision (deferred):** Raspberry Pi 5 companion computer, OpenCV target
  detection and tracking over MAVLink.

## Hardware

| Part | Component |
|------|-----------|
| Flight controller | Corvon H743 (CORVON743V1), ArduCopter 4.8.0-dev |
| ESC | Corvon 50A 4-in-1, Bluejay, DShot300 |
| Motors | Emax ECO II 2207 2400KV |
| Props | HQProp 5x4.3x3 V2S tri-blade |
| Transmitter | BetaFPV LiteRadio 3 (ELRS) |
| Receiver | RadioMaster RP3 Diversity 2.4GHz ELRS |
| Battery | 4S LiPo (Zeee 1500mAh) |
| Frame | Custom single-piece PETG center frame, plus config, carbon tube arms |
| GPS (Phase 2) | Corvon M10 |
| Companion computer (Phase 3) | Raspberry Pi 5 |

Airframe is a single-piece PETG center frame (designed in Onshape, printed on a
Bambu Lab A1) with cut carbon tube arms and printed motor mounts.

## Software / tooling

- Mission Planner — ground station, parameter config, and flight-log analysis
- ArduPilot SITL — simulation environment for mission scripting
- pymavlink — Python mission and control scripts (`drone.py`, `main.py`)
- OpenCV — target-detection prototype (`cv_detect.py`, `atlas_track.py`)
- WSL2 (Ubuntu) — development environment
- STM32CubeProgrammer — firmware flashing; esc-configurator.com — ESC config

## Repository contents

- `drone.py` — pymavlink wrapper: connect, arm, takeoff, fly_to, land, RTL
- `main.py` — example scripted mission against SITL
- `cv_detect.py` — single-image red-target detection (OpenCV)
- `cv_video_detect.py` — same detection over a video stream
- `atlas_track.py` — closes the loop: detection feeding yaw commands over MAVLink (sim)
- `log.md` — full build log, sim through first hover

## Running the simulation

```bash
# Terminal 1: launch SITL
sim_vehicle.py -v ArduCopter --console --map

# Terminal 2: run a mission
python3 main.py
```

For the tracking demo, drop a `test_video.mp4` containing a red target into the
project root and run `python3 atlas_track.py` against a running SITL instance.

## Known issues

Tracked in `KNOWN_ISSUES.md`. Current items:
- Red HSV mask in the CV code only covers hue 0–10 and misses the wrap past 179,
  so pure-red targets near the hue boundary are dropped.
- The yaw loop in `atlas_track.py` has no deadzone, causing oscillation near center.
- `drone.py` contains duplicate module-level functions alongside the `Drone` class
  (cleanup pending).

Both CV issues are Phase 3 concerns and will be fixed before hardware vision integration.
