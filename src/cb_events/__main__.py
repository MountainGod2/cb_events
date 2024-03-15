"""Run the event poller."""

import asyncio
import os

from dotenv import load_dotenv

from cb_events import CBAPIPoller

load_dotenv(override=False)


async def main() -> None:
    """Run the event poller."""
    url = os.environ.get("BASE_URL")

    async with CBAPIPoller(url) as poller:
        await poller.fetch_events()


if __name__ == "__main__":
    asyncio.run(main())
