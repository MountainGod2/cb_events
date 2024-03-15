"""Tests for the CBAPIPoller class."""

import asyncio
import contextlib
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from aiohttp import ClientResponse, ClientSession
from cb_events.poller import BaseURLError, CBAPIPoller, Event


class TestCBAPIPoller(IsolatedAsyncioTestCase):
    """Tests for the CBAPIPoller class."""

    async def asyncSetUp(self) -> None:
        """Set up the CBAPIPoller instance for testing."""
        self.url = "https://example.com/api"
        self.poller = CBAPIPoller(url=self.url)

    async def asyncTearDown(self) -> None:
        """Clean up the CBAPIPoller instance after testing."""
        await self.poller.close()

    @patch.object(ClientSession, "get")
    async def test_poll_cb_api_successful(self, mock_get: AsyncMock) -> None:
        """Test polling the API for events with a successful response."""
        # Mock response to simulate a successful API response
        mock_resp = AsyncMock()
        mock_resp.status = 200
        mock_resp.json = AsyncMock(return_value={"events": [{"id": "123", "method": "broadcastStart", "object": {}}]})

        # Correctly mimic the async context manager
        async def async_context_manager_mock(*args, **kwargs) -> AsyncMock:  # noqa: ARG001, ANN003, ANN002
            """Return the mock response as an async context manager."""
            return mock_resp

        mock_get.return_value.__aenter__ = async_context_manager_mock
        mock_get.return_value.__aexit__ = AsyncMock()  # Ensure __aexit__ returns an awaitable

        # Use AsyncMock for process_event to properly await it
        self.poller.process_event = AsyncMock()

        try:
            # Run the poller for a short time to allow for a single iteration
            task = asyncio.create_task(self.poller.poll_cb_api())
            await asyncio.sleep(0.1)  # Short sleep to let the loop iterate
        finally:
            task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await task

        # Verify process_event was called with the expected event
        assert self.poller.process_event.called  # noqa: S101
        call_arg = self.poller.process_event.call_args[0][0]
        assert isinstance(call_arg, Event)  # noqa: S101
        assert call_arg.id == "123"  # noqa: S101

    @patch.object(ClientSession, "get", new_callable=AsyncMock)
    async def test_handle_server_error(self, mock_get: AsyncMock) -> None:
        """Test handling a server error response."""
        # Prepare a mock response to simulate a server error
        mock_resp = AsyncMock(spec=ClientResponse)
        mock_resp.status = 500
        mock_get.return_value = mock_resp

        # Monitor the asyncio.sleep to simulate and verify backoff behavior
        with patch("asyncio.sleep", new_callable=AsyncMock) as mock_sleep:
            # Since handle_server_error is a coroutine, directly test it
            await self.poller.handle_server_error(mock_resp, 1)

            # Check if asyncio.sleep was called indicating a backoff
            mock_sleep.assert_called_once()

            # Verify the backoff delay is within expected bounds
            # The initial backoff delay is passed as 1, expecting it to double due to server error handling
            call_args_list = mock_sleep.call_args_list
            assert call_args_list[0][0][0] == 2, "Backoff delay did not double as expected."  # noqa: PLR2004, S101

    async def test_poll_cb_api_without_url(self) -> None:
        """Test polling the API without a URL set."""
        self.poller.url = None
        with pytest.raises(BaseURLError):
            await self.poller.poll_cb_api()

    @patch("cb_events.poller.CBAPIPoller.handle_successful_response")
    @patch("cb_events.poller.aiohttp.ClientSession.get")
    async def test_handle_response_successful(
        self,
        mock_get: AsyncMock,  # noqa: ARG002
        mock_handle_successful_response: AsyncMock,
    ) -> None:
        """Test handling a successful response."""
        # Test handling a successful response directly
        mock_resp = MagicMock(spec=ClientResponse)
        mock_resp.status = 200
        await self.poller.handle_response(mock_resp, 1)

        mock_handle_successful_response.assert_called_once()
