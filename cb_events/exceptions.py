"""Exceptions for Chaturbate poller."""
class ChaturbateAPIError(Exception):
    """Exception raised for errors in the Chaturbate API."""


class BaseURLError(Exception):
    """Raise exception when BASE_URL is missing or incorrect."""

