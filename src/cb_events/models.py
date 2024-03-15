"""Represents a Chaturbate event."""

from __future__ import annotations

from typing import Any


class Event:
    """Represents a Chaturbate event.

    Attributes:
        id: The event ID.
        method: The event method.
        object: The event object.

    """

    def __init__(self, id_: str, method_: str, object_: dict[str, Any]) -> None:
        """Initialize the event.

        Args:
            id_: The event ID.
            method_: The event method.
            object_: The event object.

        """
        self.id: str = id_
        self.method: str = method_
        self.object: dict[str, Any] = object_

    @classmethod
    def from_dict(cls, event_dict: dict[str, Any]) -> Event:
        """Create an event from a dictionary.

        Args:
            event_dict: The event dictionary.

        Returns:
            The event.

        """
        return cls(
            id_=event_dict.get("id"),
            method_=event_dict.get("method"),
            object_=event_dict.get("object"),
        )
