from enum import Enum
from typing import Dict
from datetime import datetime, timedelta


class State(Enum):
    DEFAULT = 0
    WAIT_TEXT = 1

class InMemoryStateManager:
    def __init__(self):
        self._states: Dict[str, State] = {}
        self._ttl: Dict[str, datetime] = {}

    def save_state(self, user_id: str, state: State, ttl_seconds: int = 3600):
        self._states[user_id] = state
        self._ttl[user_id] = datetime.now() + timedelta(seconds=ttl_seconds)

    def get_state(self, user_id: str) -> State:
        if user_id in self._states:
            if datetime.now() > self._ttl[user_id]:
                self.clear_state(user_id)
                return State.DEFAULT
            return self._states[user_id]
        return State.DEFAULT

    def clear_state(self, user_id: str):
        self._states.pop(user_id, None)
        self._ttl.pop(user_id, None)

storage = InMemoryStateManager()
