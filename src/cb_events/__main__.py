"""Run the event poller."""

import asyncio
import os

from dotenv import load_dotenv

from cb_events import CBAPIPoller
from cb_events.exceptions import BaseURLError

load_dotenv(override=True)


async def main() -> None:
    """Run the event poller."""
    url = os.environ.get("BASE_URL")
    if not url:
        error_msg = "Please set the BASE_URL environment variable with the correct URL."
        raise BaseURLError(error_msg)


    async with CBAPIPoller(url) as poller:
        await poller.fetch_events()


if __name__ == "__main__":
    asyncio.run(main())
