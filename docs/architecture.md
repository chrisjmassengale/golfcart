# Golf Cart Autonomous System — Architecture

## Vision
A self-driving caddie cart that follows the golfer like a dog, yields
intelligently at the ball, navigates autonomously between holes, and
provides voice-based club recommendations.
No buttons. No joystick. Just golf.

---

## System Layers

### Layer 1 — Real-time control (Teensy 4.1, ~1kHz)
- Motor PWM output
- Wheel encoder counting (odometry)
- Hardware e-stop (independent of Jetson)
- Serial/USB command interface to Jetson

Command interface (Jetson → Teensy):
  SET_VEL <linear_mps> <angular_radps>
  ESTOP
  GET_ODOM

### Layer 2 — Perception (Jetson Orin Nano Super)
Sensor fusion into world model:

| Sensor            | Data                              | Rate    |
|-------------------|-----------------------------------|---------|
| ZED 2i            | Stereo RGB, depth, IMU, person 3D | 30fps   |
| GPS (u-blox)      | Global position                   | 5Hz     |
| Wheel encoders    | Odometry (via Teensy)             | 1kHz    |
| Microphone        | Voice commands                    | cont.   |
| Temperature (I2C) | Ambient (for caddie)              | 1Hz     |

### Layer 3 — Behavior state machine (Python)
Reads world model → outputs velocity commands to Teensy.
See behavior/state_machine.py

### Layer 4 — Voice Caddie
Whisper STT → local LLM (Llama 3.1 8B) → TTS
Inputs: GPS position, hole data, distance to pin, wind, temperature
Output: club recommendation, course advice

### Layer 5 — Web Interface (FastAPI)
iPad/iPhone over Jetson WiFi hotspot.
Live depth video, mode override, telemetry, recording trigger.

---

## Behavior States

FOLLOW → SLOWING → YIELD → GREETING → FOLLOW
FOLLOW → SEARCH → FOLLOW (or WAIT)
WAIT → AUTONOMOUS_NAV → WAIT
WAIT → SLEEP → WAIT

Full state machine in behavior/state_machine.py

---

## Personality Layer

| Trigger                  | Behavior                        |
|--------------------------|---------------------------------|
| Person jogs              | Cart surges, slight overshoot   |
| Person returns to cart   | Micro forward-back greeting     |
| WAIT/YIELD > 60s         | Subtle left-right impatience    |
| Motion nearby in WAIT    | Rotate to track (curiosity)     |
| AUTONOMOUS_NAV departure | Short audio bark                |

---

## Hole Transition Logic

Triggers (all true):
1. Cart stationary near green > 90s
2. Person > 15m from green centroid
3. Person bearing matches next tee GPS waypoint
4. Person velocity > 0.8 m/s

Action: compute cart path route, match arrival timing to golfer,
visual path following via segmentation model, greet at tee.

---

## Power Architecture

24V LiFePO4 (20-30Ah)
  ├──► DC-DC 24V→12V → Motor drivers → Hub motors
  └──► DC-DC 12V→5V → Jetson + ZED + Teensy + accessories

E-stop relay on motor rail, Teensy-controlled.
Compute stays live during e-stop.

---

## Hardware Stack

| Component              | Role                        | Interface   |
|------------------------|-----------------------------|-------------|
| Jetson Orin Nano Super | Main compute                | —           |
| ZED 2i (2.1mm)         | Depth, RGB, IMU, tracking   | USB-C       |
| u-blox GPS             | Global position             | UART        |
| Teensy 4.1             | Real-time MCU, e-stop       | USB Serial  |
| Hub motors x2          | Rear wheel propulsion       | —           |
| 24V LiFePO4 battery    | Traction power              | XT60        |
| Microphone (USB)       | Voice commands              | USB         |
| Speaker                | TTS, audio cues             | USB/3.5mm   |
| Flysky FS-i6           | Manual override / training  | RF→Teensy   |
| iPad/iPhone            | Web interface               | WiFi        |

---

## Software Stack

| Layer         | Technology                          |
|---------------|-------------------------------------|
| Real-time     | C++ on Teensy                       |
| Perception    | Python, ZED SDK 5.x, TensorRT       |
| Behavior SM   | Python (behavior/state_machine.py)  |
| Path follow   | TensorRT segmentation model         |
| Voice STT     | OpenAI Whisper (local)              |
| Voice LLM     | Llama 3.1 8B (local)                |
| Voice TTS     | Piper / Kokoro                      |
| Web interface | FastAPI, WebSockets                 |
| Mapping       | ZED SDK spatial mapping + GPS       |

---

## Development Phases

Phase 1: ZED 2i bringup, person detection, path segmentation, TensorRT
Phase 2: Teensy motor control, FOLLOW PID, backyard test
Phase 3: Full state machine, hole transition, AUTONOMOUS_NAV
Phase 4: Voice caddie pipeline
Phase 5: Polish, course mapping, product demo video
