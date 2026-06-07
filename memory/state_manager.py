# memory/state_manager.py

from memory.state import state


PROJECT_KEYWORDS = [
    "project",
    "website",
    "platform",
    "app",
    "system"
]


def update_state(user_message: str):
    text = user_message.lower()

    if "tourism" in text:
        state.active_project = "Tourism Platform"

    if "research" in text:
        state.current_goal = "Research"

    if "booking" in text:
        state.current_topic = "Booking System"