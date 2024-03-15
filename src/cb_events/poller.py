"""Poller for Chaturbate API.

This module provides the following classes and functions:

- CBAPIPoller: Poller for the Chaturbate API.
- Event: Represents a Chaturbate event.
- EventFormatter: Formats Chaturbate events as messages.
- log_events: Logs events.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Callable

import aiohttp
from aiolimiter import AsyncLimiter
from typing_extensions import Self

from cb_events.event_formatter import EventFormatter
from cb_events.exceptions import BaseURLError, ChaturbateAPIError
from cb_events.models import Event

SERVER_ERROR = (501, 502, 521)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(message)s",
    datefmt="%d %b %Y %H:%M:%S",
)

SERVER_ERROR = {500, 502, 503, 504}  # Define the set of server error status codes


class CBAPIPoller:
    """Poller for Chaturbate API."""

    def __init__(
        self,
        url: str | None = None,
        rate_limit: int = 2000,
        session: aiohttp.ClientSession | None = None,
    ) -> None:
        """Initialize the poller."""
        self.url: str | None = url
        self.rate_limit: int = rate_limit
        self.session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self.event_callback: Callable[[Any], None] | None = None
        self.max_backoff_delay: int = 60  # Maximum backoff delay (in seconds)

    async def __aenter__(self: Self) -> Self:
        """Enter the poller context."""
        return self

    async def __aexit__(self, *args: object) -> None:
        """Exit the poller context."""
        await self.close()

    async def close(self) -> None:
        """Close the session."""
        if self.session:
            await self.session.close()

    async def poll_cb_api(self) -> None:
        """Poll the Chaturbate API."""
        limiter = AsyncLimiter(self.rate_limit)
        backoff_delay: int = 1  # Initial backoff delay
        if not self.url:
            msg = "Please set the BASE_URL environment variable with the correct URL."
            raise BaseURLError(msg)

        logging.debug("Polling Chaturbate API at %s", self.url)
        try:
            while True:
                async with limiter, self.session.get(self.url) as response:
                    await self.handle_response(response, backoff_delay)
                    backoff_delay = 1  # Reset backoff on success
        except aiohttp.ClientError as e:
            logging.exception("An error occurred during API polling")
            raise ChaturbateAPIError from e

    async def handle_response(
        self,
        response: aiohttp.ClientResponse,
        backoff_delay: int,
    ) -> None:
        """Handle the response."""
        if response.status == aiohttp.http.HTTPStatus.OK:
            await self.handle_successful_response(response)
            backoff_delay = 1  # Reset backoff on success
        elif response.status in SERVER_ERROR:
            await self.handle_server_error(response, backoff_delay)
        else:
            response.raise_for_status()

    async def handle_successful_response(
        self,
        response: aiohttp.ClientResponse,
    ) -> None:
        """Handle successful response."""
        json_response: dict[str, Any] = await response.json()
        for message in json_response.get("events", []):
            event: Any = Event.from_dict(message)
            await self.process_event(event)

        # Use nextUrl from response for the next request
        if "nextUrl" in json_response:
            self.url = json_response["nextUrl"]

    async def handle_server_error(
        self,
        response: aiohttp.ClientResponse,
        backoff_delay: int,
    ) -> None:
        """Handle server errors."""
        backoff_delay *= 2
        backoff_delay = min(backoff_delay, self.max_backoff_delay)  # Limiting backoff delay
        logging.warning(
            "Server error %s, retrying in %s seconds",
            response.status,
            backoff_delay,
        )
        await asyncio.sleep(backoff_delay)

    async def process_event(self, event: Event) -> None:
        """Process the event."""
        if self.event_callback:
            await self.event_callback(event)
        else:
            await log_events(event)

    async def fetch_events(
        self,
        event_callback: Callable[[Any], None] | None = None,
    ) -> None:
        """Fetch events from the Chaturbate API."""
        self.event_callback = event_callback
        await self.poll_cb_api()


async def log_events(event: Event) -> None:
    """Log events."""
    formatter: EventFormatter = EventFormatter(event.id, event.method, event.object)
    formatted_message = formatter.format_as_message()
    logging.info(formatted_message)
