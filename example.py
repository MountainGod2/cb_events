import asyncio  # noqa: D100

from cb_events import CBAPIPoller, log_events


async def main() -> None:  # noqa: D103
    url = "https://eventsapi.chaturbate.com/events/mrslaw/JAzuRHJWcoVcHjIDLs7bjNlQ/"
    async with CBAPIPoller(url) as poller:
        await poller.fetch_events(event_callback=log_events)

if __name__ == "__main__":
    asyncio.run(main())
