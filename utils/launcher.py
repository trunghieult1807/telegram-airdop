import os
import glob
from pyrogram import Client
from utils.config import settings
import json
import asyncio
from coinsweeper.core.tapper import run_tapper as coinsweeper
from tomarket.core.tapper import run_tapper as tomarket
from okxracer.core.tapper import run_tapper as okxracer
from notpixel.core.tapper import run_tapper as notpixel
from seed.core.tapper import run_tapper as seed

def get_session_names() -> list[str]:
    session_names = sorted(glob.glob("sessions/*.session"))
    session_names = [
        os.path.splitext(os.path.basename(file))[0] for file in session_names
    ]

    return session_names

async def get_tg_clients(app_name: str) -> list[Client]:
    session_names = get_session_names()

    if not session_names:
        raise FileNotFoundError("Not found session files")

    try:
        with open('config.json', 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        json_data = {}
        
    tg_clients = []
    for session_name in session_names:        
        api_id = os.getenv(f"{session_name.upper()}_API_ID") or settings.API_ID
        api_hash = os.getenv(f"{session_name.upper()}_API_HASH") or settings.API_HASH
            
        if not api_id or not api_hash:
            raise ValueError(f"API_ID and API_HASH not found for session: {session_name}")

        client = Client(
            name=session_name,
            api_id=api_id,
            api_hash=api_hash,
            workdir="sessions/",
        )
        if json_data.get(session_name) and json_data.get(session_name).get(app_name) == 0:
            continue
        else:
            tg_clients.append(client)
        

    return tg_clients

async def create_tasks(app_name: str) -> list[asyncio.Task]:
    tg_clients = await get_tg_clients(app_name)
    if app_name == "coinsweeper":
        target_function = coinsweeper
    elif app_name == "tomarket":
        target_function = tomarket
    elif app_name == "okxracer":
        target_function = okxracer
    elif app_name == "notpixel":
        target_function = notpixel
    elif app_name == "seed":
        target_function = seed
    return [
        asyncio.create_task(
            target_function(
                tg_client=tg_client,
                proxy=None,
            )
        )
        for tg_client in tg_clients
    ]