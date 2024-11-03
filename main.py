import asyncio
from contextlib import suppress

from utils.launcher import create_tasks, get_tg_clients
from dotenv import load_dotenv

async def main():
    load_dotenv()
    tg_clients = await get_tg_clients()
    await asyncio.gather(
        *await create_tasks("coinsweeper", tg_clients),
        *await create_tasks("notpixel", tg_clients),
        *await create_tasks("okxracer", tg_clients),
        # *await create_tasks("tomarket", tg_clients),
        *await create_tasks("seed", tg_clients),
        *await create_tasks("memefi", tg_clients),
        *await create_tasks("blum", tg_clients),
    )


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
