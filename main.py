import asyncio
from contextlib import suppress

from utils.launcher import create_tasks, get_tg_clients
from dotenv import load_dotenv

async def main():
    load_dotenv()
    tg_clients = get_tg_clients()
    await asyncio.gather(*await create_tasks(tg_clients))


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
