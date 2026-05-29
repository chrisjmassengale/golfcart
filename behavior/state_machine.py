"""
Golf Cart Behavior State Machine

States: FOLLOW, SLOWING, YIELD, GREETING, WAIT, SEARCH, AUTONOMOUS_NAV, SLEEP
Inputs: world model (person position/velocity, GPS, obstacles)
Output: velocity commands to Teensy layer
"""

from enum import Enum, auto
import time
import math


class State(Enum):
    FOLLOW = auto()
    SLOWING = auto()
    YIELD = auto()
    GREETING = auto()
    WAIT = auto()
    SEARCH = auto()
    AUTONOMOUS_NAV = auto()
    SLEEP = auto()


class GolfCartStateMachine:
    SLOW_VEL_THRESHOLD = 0.3       # m/s
    PERSON_LOST_TIMEOUT = 3.0      # s
    SEARCH_TIMEOUT = 30.0          # s
    IMPATIENCE_TIMEOUT = 60.0      # s
    SLEEP_TIMEOUT = 300.0          # s
    FOLLOW_OFFSET_M = 1.5          # m
    FOLLOW_BEARING_DEG = 270.0     # deg (golfer's left)
    YIELD_OFFSET_M = 3.0           # m
    GREETING_DURATION = 1.5        # s

    def __init__(self):
        self.state = State.FOLLOW
        self.state_entry_time = time.time()
        self.person_last_seen = time.time()

    def transition(self, new_state: State):
        print(f"[SM] {self.state.name} → {new_state.name}")
        self.state = new_state
        self.state_entry_time = time.time()

    def time_in_state(self) -> float:
        return time.time() - self.state_entry_time

    def update(self, world_model: dict) -> dict:
        """
        world_model keys:
          person_detected: bool
          person_distance: float (m)
          person_velocity: float (m/s)
          person_bearing: float (deg)
          person_stopped_near_ball: bool
          hole_complete: bool
          voice_command: str | None
          obstacle_detected: bool
          arrived_at_waypoint: bool
        returns:
          cmd: dict with linear_mps, angular_radps, audio_cue
        """
        cmd = {"linear_mps": 0.0, "angular_radps": 0.0, "audio_cue": None}

        if world_model.get("person_detected"):
            self.person_last_seen = time.time()

        person_lost_duration = time.time() - self.person_last_seen
        voice = world_model.get("voice_command")

        if self.state == State.FOLLOW:
            if voice == "stop":
                self.transition(State.WAIT)
            elif not world_model.get("person_detected") and person_lost_duration > self.PERSON_LOST_TIMEOUT:
                self.transition(State.SEARCH)
            elif world_model.get("hole_complete"):
                self.transition(State.AUTONOMOUS_NAV)
            elif world_model.get("person_velocity", 1.0) < self.SLOW_VEL_THRESHOLD:
                self.transition(State.SLOWING)
            else:
                cmd = self._follow_cmd(world_model)

        elif self.state == State.SLOWING:
            if world_model.get("person_velocity", 1.0) >= self.SLOW_VEL_THRESHOLD:
                self.transition(State.FOLLOW)
            elif world_model.get("person_stopped_near_ball"):
                self.transition(State.YIELD)
            else:
                cmd["linear_mps"] = 0.3

        elif self.state == State.YIELD:
            if voice == "follow" or world_model.get("person_velocity", 0) > self.SLOW_VEL_THRESHOLD:
                self.transition(State.GREETING)
            else:
                wiggle = 0.15 * math.sin(time.time() * 1.5) if self.time_in_state() > self.IMPATIENCE_TIMEOUT else 0.0
                cmd["angular_radps"] = wiggle

        elif self.state == State.GREETING:
            if self.time_in_state() > self.GREETING_DURATION:
                self.transition(State.FOLLOW)
            else:
                cmd["linear_mps"] = 0.2 * math.sin(self.time_in_state() * math.pi * 2 / self.GREETING_DURATION)

        elif self.state == State.WAIT:
            if voice == "follow":
                self.transition(State.FOLLOW)
            elif world_model.get("hole_complete"):
                self.transition(State.AUTONOMOUS_NAV)
            elif world_model.get("person_detected") and world_model.get("person_distance", 99) < 2.0:
                self.transition(State.GREETING)
            elif self.time_in_state() > self.SLEEP_TIMEOUT:
                self.transition(State.SLEEP)

        elif self.state == State.SEARCH:
            if world_model.get("person_detected"):
                self.transition(State.FOLLOW)
            elif self.time_in_state() > self.SEARCH_TIMEOUT:
                self.transition(State.WAIT)
            else:
                cmd = {"linear_mps": 0.0, "angular_radps": 0.3, "audio_cue": "search_whimper.wav"}

        elif self.state == State.AUTONOMOUS_NAV:
            if world_model.get("arrived_at_waypoint"):
                self.transition(State.WAIT)
            else:
                cmd = {"linear_mps": 1.2, "angular_radps": 0.0, "audio_cue": None}

        elif self.state == State.SLEEP:
            if voice or world_model.get("person_detected"):
                self.transition(State.WAIT)

        return cmd

    def _follow_cmd(self, wm) -> dict:
        # TODO: PID on bearing and distance error
        # Personality: overshoot on acceleration (dog surge)
        return {"linear_mps": 0.8, "angular_radps": 0.0, "audio_cue": None}
