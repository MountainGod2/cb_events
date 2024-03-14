# Chaturbate Events

Chaturbate Events is a Python package for fetching and processing events from the Chaturbate API.

## Installation

You can install Chaturbate Events using pip, creating a virtual enviroment if needed:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install cb-events
```

## Usage

To fetch events from the Chaturbate API, you can use the fetch_events function provided by the package. Here's an example of how to use it:

```python
import asyncio

from cb_events import CBAPIPoller


async def main() -> None:
    url = "https://eventsapi.chaturbate.com/events/YOUR_USERNAME/******************/"
    async with CBAPIPoller(url) as poller:
        await poller.fetch_events()

if __name__ == "__main__":
    asyncio.run(main())

```

> [!NOTE]
> Replace "https://eventsapi.chaturbate.com/events/YOUR_USERNAME/******************/" with the appropriate URL.

Alternatively, you can set an enviroment variable in an .env file, and run the program as a module.

```bash
echo BASE_URL='"https://eventsapi.chaturbate.com/events/YOUR_USERNAME/******************"' >> ./.env
python3 -m cb_events
```

## Contributing

Contributions are welcome! If you encounter any bugs or have suggestions for improvements, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.