# memory/state.py

from dataclasses import dataclass


@dataclass
class SessionState:
    current_topic: str | None = None
    active_project: str | None = None
    current_goal: str | None = None
    pending_action: dict | None = None


state = SessionState()