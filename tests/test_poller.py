"""Test cases for the CBAPIPoller class."""
import asyncio
import unittest
from unittest.mock import AsyncMock, patch

import pytest
from cb_events.exceptions import BaseURLError
from cb_events.models import Event
from cb_events.poller import SERVER_ERROR, CBAPIPoller


class TestCBAPIPoller(unittest.TestCase):
    """Test cases for the CBAPIPoller class."""

    def setUp(self) -> None:
        """Test cases setup."""
        self.poller = CBAPIPoller(url="https://fakeurl.com/api")
        self.session_patch = patch("aiohttp.ClientSession", autospec=True)
        self.mock_session = self.session_patch.start()
        self.addCleanup(self.session_patch.stop)

    async def test_aenter_and_aexit(self) -> None:
        """Test the context manager behavior."""
        async with CBAPIPoller() as poller:
            assert poller.session is not None
        assert poller.session.close.called

    async def test_poll_cb_api_without_url(self) -> None:
        """Test polling without URL raises BaseURLError."""
        poller = CBAPIPoller()  # URL is not set
        with pytest.raises(BaseURLError):
            await poller.poll_cb_api()

    @patch("cb_events.poller.CBAPIPoller.handle_response")
    async def test_poll_cb_api_success(self, mock_handle_response: AsyncMock) -> None:
        """Test successful API polling and response handling."""
        mock_response = AsyncMock()
        self.mock_session.get.return_value.__aenter__.return_value = mock_response
        mock_response.status = 200
        await self.poller.poll_cb_api()
        mock_handle_response.assert_called_with(mock_response, 1)

    async def test_handle_successful_response(self) -> None:
        """Test handling of successful response."""
        event_data = {
            "id": "test_id",
            "method": "test_method",
            "object": "test_object",
        }
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "events": [event_data],
            "nextUrl": "https://fakeurl.com/api/next",
        }
        await self.poller.handle_successful_response(mock_response)
        assert self.poller.url == "https://fakeurl.com/api/next"

    async def test_handle_server_error(self) -> None:
        """Test handling of server error with backoff."""
        mock_response = AsyncMock()
        mock_response.status = SERVER_ERROR[0]
        with patch("asyncio.sleep", side_effect=asyncio.TimeoutError) as mock_sleep:
            with pytest.raises(asyncio.TimeoutError):
                await self.poller.handle_server_error(mock_response, 1)
            mock_sleep.assert_called_with(2)

    async def test_process_event_with_callback(self) -> None:
        """Test event processing with a custom callback."""
        event_callback = AsyncMock()
        self.poller.event_callback = event_callback
        event = Event(id="test", method="GET", object="data")
        await self.poller.process_event(event)
        event_callback.assert_called_once_with(event)

    @patch("cb_events.poller.log_events", new_callable=AsyncMock)
    async def test_process_event_without_callback(self, mock_log_events: AsyncMock) -> None:
        """Test event processing falls back to logging when no callback is provided."""
        event = Event(id="test", method="GET", object="data")
        await self.poller.process_event(event)
        mock_log_events.assert_called_once_with(event)

if __name__ == "__main__":
    unittest.main()
