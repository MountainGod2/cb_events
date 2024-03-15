"""Format Chaturbate events as messages."""

from __future__ import annotations

from typing import Any


class EventFormatter:
    """Format Chaturbate events as messages.

    Attributes:
        id: The event ID.
        method: The event method.
        object: The event object.

    """

    def __init__(self, event_id: str, method: str, obj: dict[str, Any]) -> None:
        """Initialize the event formatter.

        Args:
            event_id: The event ID.
            method: The event method.
            obj: The event object.

        """
        self.id: str = event_id
        self.method: str = method
        self.object: dict[str, Any] = obj

    def format_as_message(self) -> str:
        """Format the event as a message.

        Returns:
            The formatted message.

        """
        user = self.object.get("user", {}).get("username", "")
        message = self.object.get("message", {}).get("message", "")
        tokens = self.object.get("tip", {}).get("tokens", "")
        is_anon = self.object.get("tip", {}).get("isAnon", False)
        tip_message = (
            self.object.get("tip", {}).get("message", "")[3:]
            if self.object.get("tip", {}).get("message", "").startswith(" | ")
            else ""
        )

        message_mappings: dict[str, str] = {
            "broadcastStart": "Broadcast started",
            "broadcastStop": "Broadcast stopped",
            "userEnter": f"{user} entered the room",
            "userLeave": f"{user} left the room",
            "follow": f"{user} has followed",
            "unfollow": f"{user} has unfollowed",
            "fanclubJoin": f"{user} joined the fan club",
            "chatMessage": f"{user} sent chat message: {message}",
            "privateMessage": (
                f"{self.object.get('message', {}).get('fromUser', '')}"
                f" sent private message to {self.object.get('message', {}).get('toUser', '')}:"
                f" {self.object.get('message', {}).get('message', '')}"
            ),
            "tip": (
                f"{user} sent {tokens} tokens {'anonymously ' if is_anon else ''}"
                f"{'with message: ' + tip_message if tip_message else ''}"
            ),
            "roomSubjectChange": f"Room Subject changed to {self.object.get('subject', '')}",
            "mediaPurchase": (
                f"{user} purchased {self.object.get('media', {}).get('type', '')}"
                f" set: {self.object.get('media', {}).get('name', '')}"
            ),
        }
        return message_mappings.get(self.method, "Unknown event")
