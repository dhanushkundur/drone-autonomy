# ATLAS

**Autonomous Tracking and Landing Aerial System**

A 5-inch class autonomous quadcopter built from the frame up. Custom CAD, custom firmware configuration, Python flight control via MAVLink, and an OpenCV vision pipeline for target tracking.

Built by [Dhanush Kundur](https://github.com/<your-handle>), mechanical engineering at Ohio State. Targeting robotics and defense autonomy.

---

## Project phases

Build strategy is **flight-first**: prove manual hover before adding autonomy, prove autonomy before adding vision. Every phase is gated by the previous one working.

- **Phase 1: Simulation** *(complete)* — ArduPilot SITL, pymavlink, scripted takeoff / waypoint navigation / RTL / landing
- **Phase 2: Vision pipeline** *(complete in sim)* — OpenCV HSV detection on image and video, yaw-rate control loop closing detection to MAVLink commands in SITL
- **Phase 3: Hardware build** *(in progress)* — frame design, motor mount iteration, FC/ESC stack assembly, manual hover
- **Phase 4: Autonomous hover and waypoints on hardware** *(pending)*
- **Phase 5: Vision tracking on hardware** *(pending)* — port pipeline to Raspberry Pi 5 + Pi Camera 3 Wide, integrate with companion-computer MAVLink link

---

## Hardware

| Component | Part |
|---|---|
| Flight controller | Corvon H743 (ArduPilot `CORVON743V1`) |
| ESC | Corvon 50A 4-in-1 BLHeli_S |
| Motors | Emax ECO II 2207 2400KV |
| Frame | Custom 100x100mm octagonal dual-plate PETG, 16mm OD carbon fiber tube arms |
| Battery | CNHL Black Series 4S 1500mAh 100C |
| Radio | RadioMaster Pocket ELRS + BetaFPV ELRS Lite Rx |
| GPS | Matek M10Q-5883 *(deferred)* |
| Companion computer | Raspberry Pi 5 4GB *(deferred)* |
| Camera | Pi Camera Module 3 Wide *(deferred)* |

Frame and motor mounts designed in Onshape. Printed in PETG with annealed walls for arm-socket strength.

---

## Software

| File | Role |
|---|---|
| `drone.py` | `Drone` class wrapping MAVLink: connect, arm, takeoff, fly_to, land, RTL |
| `main.py` | Minimal scripted mission demo |
| `cv_detect.py` | Single-frame HSV red-target detection |
| `cv_video_detect.py` | Frame-by-frame detection on a video stream |
| `atlas_track.py` | Closes the loop: detection error drives proportional yaw commands to the FC |
| `log.md` | Dev log |

**Environment:** WSL2 Ubuntu 22.04, Python 3, ArduPilot SITL, Mission Planner (ground station on Windows), VS Code.

---

## Running the simulation

```bash
# Terminal 1: launch SITL
sim_vehicle.py -v ArduCopter --console --map

# Terminal 2: run a mission
python3 main.py
```

For the tracking demo, drop a `test_video.mp4` containing a red target into the project root and run `python3 atlas_track.py` against a running SITL instance.

---

## Known issues

Documented in `KNOWN_ISSUES.md`. Short version: red HSV mask only covers hue 0 to 10 (misses wrap past 179), and the yaw loop in `atlas_track.py` has no deadzone, causing oscillation near center. Both fixed before hardware integration.

---

## Status

Currently in Phase 3. Carbon tubes fit-tested, motor mount geometry finalized pending motor arrival, FC/ESC stack hardware on order. First powered hover target: end of summer 2026.
