from core.client import Client
import asyncio
from contextlib import suppress

from logger.logger import logger

async def register_sessions() -> None:
    session_name = input('\nEnter the session name (press Enter to exit): ')

    if not session_name:
        return None

    session = Client(session_name)

    async with session:
        user_data = await session.get_me()

    logger.bind(tag="SYSTEM").success(f'Session added successfully @{user_data.username} | {user_data.first_name} {user_data.last_name}')

async def main():
    await register_sessions()


if __name__ == '__main__':
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
