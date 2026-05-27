# AI Golf Cart

Autonomous golf cart build on CaddyTek 3-wheel frame.

**Compute**: NVIDIA Jetson Orin Nano Super  
**Perception**: Waveshare IMX219-83 Stereo Camera + ICM20948 IMU  
**Stack**: GStreamer, OpenCV, TensorRT, Python

## Phases
- Phase 1: Monocular segmentation — drivable path detection
- Phase 2: Stereo depth — obstacle ranging + visual-inertial odometry

## Structure
- perception/ — inference pipelines
- firmware/ — real-time MCU layer
- calibration/ — stereo calibration scripts and outputs
- models/ — TensorRT engines and ONNX files
- data/ — sensor logs (gitignored)
- docs/ — wiring diagrams, build notes
- scripts/ — utilities and setup automation
