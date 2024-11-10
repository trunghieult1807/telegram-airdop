import os
import glob
import json
import asyncio
from core.client import Client
from coinsweeper.core.tapper import run_tapper as coinsweeper
from tomarket.core.tapper import run_tapper as tomarket
from okxracer.core.tapper import run_tapper as okxracer
from notpixel.core.tapper import run_tapper as notpixel
from seed.core.tapper import run_tapper as seed
from memefi.core.tapper import run_tapper as memefi
from blum.core.tapper import run_tapper as blum

def get_session_names() -> list[str]:
    session_names = sorted(glob.glob("sessions/*.session"))
    session_names = [
        os.path.splitext(os.path.basename(file))[0] for file in session_names
    ]

    return session_names

async def get_tg_clients() -> list[Client]:
    session_names = get_session_names()

    if not session_names:
        raise FileNotFoundError("Not found session files")
    
    return [Client(session_name) for session_name in session_names]

async def create_tasks(app_name: str, tg_clients: list[Client]) -> list[asyncio.Task]:
    app_functions = {
        "coinsweeper": coinsweeper,
        "tomarket": tomarket,
        "okxracer": okxracer,
        "notpixel": notpixel,
        "seed": seed,
        "memefi": memefi,
        "blum": blum,
    }

    target_function = app_functions.get(app_name)
    if not target_function:
        raise ValueError(f"Unknown app name: {app_name}")

    try:
        with open('config.json', 'r') as file:
            json_data = json.load(file)
    except Exception as e:
        json_data = {}

    return [
        asyncio.create_task(target_function(tg_client=tg_client, proxy=None))
        for tg_client in tg_clients
        if json_data.get(tg_client.name) is None or json_data.get(tg_client.name).get(app_name) != 0
    ]
