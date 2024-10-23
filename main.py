import asyncio
from contextlib import suppress

from utils.launcher import get_tg_clients
from tomarket.utils.launcher import create_tasks as tomarket

from dotenv import load_dotenv

async def main():
    load_dotenv()
    await asyncio.gather(
        *tomarket(await get_tg_clients("tomarket")),
    )


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
