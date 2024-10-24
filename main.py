import asyncio
from contextlib import suppress

from utils.launcher import create_tasks
from dotenv import load_dotenv

async def main():
    load_dotenv()
    await asyncio.gather(
        # *await create_tasks("tomarket"),
        # *await create_tasks("coinsweeper"),
        # *await create_tasks("okxracer"),
        *await create_tasks("notpixel"),
    )


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
