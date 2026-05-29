# Project Context & Decision Log

Last updated: May 2026
Use this file to onboard a new conversation instantly.

---

## What This Is

Autonomous AI golf caddie cart built on a CaddyTek 3-wheel push cart frame.
Not remote-controlled. Fully autonomous — follows the golfer like a dog,
yields at the ball, navigates between holes independently.
No buttons. No joystick. Just golf.

Dual purpose:
1. Deep edge-AI real-time systems experience (primary goal)
2. Real product concept with defensible market

---

## Hardware Purchased

| Item | Cost | Status |
|------|------|--------|
| NVIDIA Jetson Orin Nano Super | ~$250 | In hand, configured |
| ZED 2i (2.1mm, IR-cut, IP66) | $265 eBay | Shipping from Utah |

---

## Jetson Environment

- JetPack: 6.2 / L4T R36.4.7
- OpenCV: 4.8.0 + GStreamer 1.20.3 (confirmed working)
- numpy: pinned <2.0 (do NOT upgrade — breaks OpenCV)
- ZED SDK: installed via diagnostic tool, AI models downloading
- SSH: working from Mac mini M4 Pro
- VS Code Remote SSH: configured
- Storage: 196GB free, 256GB SanDisk Extreme U3 SD card
- Repo: github.com/chrisjmassengale/golfcart (public)

---

## Next Order

- Teensy 4.1 ~$32
- Flysky FS-i6 RC transmitter ~$40
- Bench supply 30V/5A used ~$80-110
- USB-C PD supply for Orin ~$20
- u-blox GPS ~$30

---

## Drivetrain — Pending

CaddyTek measurements (rough):
- Independent rear axles, ~0.5 inch steel per wheel
- Wheel diameter: ~12 inches

Independent axles = hub motors viable, no differential fab needed.
Next: measure hub ID and axle-to-frame clearance.
Candidates: Bafang 12-inch hub motors + ODrive S1 or Cytron MDD10A driver.

---

## Power Architecture

24V LiFePO4 (20-30Ah) → DC-DC 24→12V → motors
                       → DC-DC 12→5V → Jetson + ZED + Teensy
E-stop relay on motor rail, Teensy-controlled.
LiFePO4 chosen over LiPo: outdoor unsupervised vehicle, thermal safety.

---

## Key Camera Decision

ZED 2i chosen over: Waveshare IMX219 (returned, no sync), OAK-D,
RealSense D455, Orbbec Gemini 335L, ZED X Stereo ($780 all-in),
Ouster Rev8 (industrial pricing, not available).

Why ZED 2i: person tracking + spatial mapping built into SDK (load-bearing
for follow/yield behavior), 120mm baseline, IP66, USB-C plug-and-play,
ZED SDK 5.3 confirmed on JetPack 6.2, Stereolabs builds products around
Orin Nano. 2.1mm lens confirmed from photo. IR-cut confirmed from coating.

---

## Behavior State Machine

States: FOLLOW → SLOWING → YIELD → GREETING → FOLLOW
        FOLLOW → SEARCH → FOLLOW/WAIT
        WAIT → AUTONOMOUS_NAV → WAIT
        WAIT → SLEEP → WAIT

Key behaviors:
- FOLLOW: 1.5m left, pace match, dog-like acceleration overshoot
- YIELD: peel to non-ball side, 3m offset, clear swing path
- GREETING: micro forward-back wiggle on return
- AUTONOMOUS_NAV: cart path to next tee, arrives 30s before golfer
- SLEEP: low power after 5min idle

Personality: impatience wiggle (60s), curiosity tracking,
audio bark on departure, greeting surge on jog.

Full implementation: behavior/state_machine.py

---

## 3D Printing

- Printer: Prusa i3 MK3
- Material: PETG (UV stable, 80°C+, impact resistant)
- PLA rejected: warps in direct California sun
- First print target: ZED 2i mount bar for CaddyTek frame tube
- Structural motor mounts: aluminum plate

---

## Field Operation

Jetson hotspot "GolfCart" → iPad Safari → http://192.168.4.1:5000
Live depth/RGB video, mode override, recording trigger, telemetry.
RC transmitter (Flysky FS-i6) for manual drive during training.

---

## Next Session Priorities

1. ZED 2i arrives → ZED_Explorer → confirm stream
2. ZED Python bindings → person detection sample
3. Stream live depth video to iPad over hotspot
4. Measure CaddyTek hub ID + axle clearance → spec hub motors
5. Order Teensy 4.1, Flysky, bench supply
6. Begin FOLLOW PID in behavior/state_machine.py

---

## About the Builder

Chris, Principal Engineer, medical device startup (Anaxiom Inc, OC CA).
Background: firmware, embedded, mechanical engineering, cryogenic systems.
Built motorized camera slider in college — this is the spiritual successor.
Moving: Coto de Caza → Newport Beach/Costa Mesa.
Goal: edge-AI real-time systems experience → career leverage + product company.
