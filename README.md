# AI Golf Cart

Autonomous golf caddie cart on CaddyTek 3-wheel frame.

**Compute**: NVIDIA Jetson Orin Nano Super  
**Perception**: ZED 2i Stereo Camera (2.1mm, IP66) + integrated IMU  
**Stack**: ZED SDK 5.x, GStreamer, OpenCV, TensorRT, Python, FastAPI

## Vision
No buttons. No joystick. Just golf. The cart follows the golfer like a dog,
yields at the ball, and navigates autonomously to the next tee.

## Phases
- Phase 1: Person detection + 3D tracking, drivable path segmentation
- Phase 2: FOLLOW/YIELD/WAIT behavior state machine, PID controller
- Phase 3: Hole transition + autonomous cart path navigation
- Phase 4: Voice caddie (Whisper STT + local LLM + TTS)
- Phase 5: Polish, course mapping, product demo

## Planned Features
- Follow mode — 1.5m left of golfer, pace match, dog-like personality
- Yield at ball — peel to non-interference side, clear of swing path
- Autonomous hole navigation — cart meets you at the next tee
- Voice LLM caddie — club suggestions, distance to pin, wind, conditions
- Voice commands — follow, stop, navigate, return
- iPad/iPhone web interface via Jetson WiFi hotspot
- Dog personality — greeting wiggle, impatience sway, curiosity tracking

## Structure
- perception/ — inference pipelines (phase1: segmentation, phase2: stereo)
- behavior/ — state machine (FOLLOW, SLOWING, YIELD, GREETING, WAIT, SEARCH, AUTONOMOUS_NAV, SLEEP)
- firmware/ — Teensy real-time layer (motor PWM, encoders, e-stop)
- calibration/ — stereo calibration scripts
- models/ — TensorRT engines (gitignored)
- data/ — sensor logs (gitignored)
- webapp/ — FastAPI phone/tablet interface
- docs/ — architecture, hardware list, setup guides
- scripts/ — utilities

## Docs
- docs/architecture.md — full system architecture and sensor fusion design
- docs/hardware_list.md — hardware status and next orders
- docs/hotspot_setup.md — Jetson WiFi hotspot for field use
- CONTEXT.md — full project state and decision log
