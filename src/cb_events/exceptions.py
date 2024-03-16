"""Exceptions for the cb_events package."""


class ChaturbateAPIError(Exception):
    """Exception raised for errors in the Chaturbate API.

    Attributes:
        message -- explanation of the error
    """


class BaseURLError(Exception):
    """Raise exception when BASE_URL is missing or incorrect.

    Attributes:
        message -- explanation of the error
    """
