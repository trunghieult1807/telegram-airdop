import asyncio
from contextlib import suppress

from utils.launcher import get_tg_clients, launch
from dotenv import load_dotenv

async def main():
    load_dotenv()
    tg_clients = get_tg_clients()
    await launch(tg_clients)


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
