import asyncio  # noqa: D100, INP001

from cb_events.poller import CBAPIPoller, log_events


async def main() -> None:  # noqa: D103
    url = "https://eventsapi.chaturbate.com/events/USER_NAME/API_KEY/"
    async with CBAPIPoller(url) as poller:
        await poller.fetch_events(event_callback=log_events)


if __name__ == "__main__":
    asyncio.run(main())
