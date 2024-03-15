"""Represents a Chaturbate event."""
from __future__ import annotations

from typing import Any


class Event:
    """Represents a Chaturbate event."""

    def __init__(self, id_: str, method_: str, object_: dict[str, Any]) -> None:
        """Initialize the event."""
        self.id: str = id_
        self.method: str = method_
        self.object: dict[str, Any] = object_

    @classmethod
    def from_dict(cls, event_dict: dict[str, Any]) -> Event:
        """Create an event from a dictionary."""
        return cls(
            id_=event_dict.get("id"),
            method_=event_dict.get("method"),
            object_=event_dict.get("object"),
        )

