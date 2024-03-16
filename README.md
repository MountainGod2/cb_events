# Chaturbate Events

Chaturbate Events is a Python package for fetching and processing events from the Chaturbate API.

## Installation

You can install Chaturbate Events using pip (creating a virtual environment if needed):

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install cb-events
```

## Usage

To fetch events from the Chaturbate API, you can use the `fetch_events` function provided by the package.

This function supports an optional callback if you wish to perform your logic when receiving events. By default, it defaults to logging the events as formatted messages.

Here's an example of how to use it:

```python
import asyncio

from cb_events.poller import CBAPIPoller


async def main() -> None:
    url = "https://eventsapi.chaturbate.com/events/USER_NAME/API_KEY/"

    async with CBAPIPoller(url) as poller:
        # Supports optional callback, defaults to logging events
        await poller.fetch_events(event_callback=log_events)

if __name__ == "__main__":
    asyncio.run(main())

```

> [!NOTE]
> Replace "https://eventsapi.chaturbate.com/events/USER_NAME/API_KEY/" with your actual events API URL.

Alternatively, you can set an environment variable in a .env file, and run the program as a module.

```bash
echo BASE_URL='"https://eventsapi.chaturbate.com/events/USER_NAME/API_KEY"' >> ./.env
python3 -m cb_events
```

## Contributing

Contributions are welcome! If you encounter any bugs or have suggestions for improvements, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
