# AI Golf Cart

Autonomous golf cart on CaddyTek 3-wheel frame.

**Compute**: NVIDIA Jetson Orin Nano Super  
**Perception**: Waveshare IMX219-83 Stereo Camera + ICM20948 IMU  
**Stack**: GStreamer, OpenCV, TensorRT, Python, FastAPI

## Phases
- Phase 1: Monocular segmentation — drivable path detection
- Phase 2: Stereo depth — obstacle ranging + visual-inertial odometry

## Planned Features
- Voice LLM caddie (club suggestions, distance to hazards/green, wind)
- Voice commands for cart modes (follow, navigate, stop, return)
- iPhone/iPad web interface via Jetson WiFi hotspot
- RC transmitter for manual drive during training sessions

## Structure
- perception/ — inference pipelines
- firmware/ — real-time MCU layer
- calibration/ — stereo calibration scripts
- models/ — TensorRT engines (gitignored)
- data/ — sensor logs (gitignored)
- docs/ — setup guides, hardware list, wiring
- webapp/ — FastAPI phone/tablet interface
- scripts/ — utilities

## Docs
- docs/hotspot_setup.md — field WiFi config
- docs/hardware_list.md — hardware status and next orders
