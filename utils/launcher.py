import os
import glob
import asyncio
from core.client import Client
from core.config import Config
from logger.logger import glogger
from coinsweeper.core.tapper import run_tapper as coinsweeper
from tomarket.core.tapper import run_tapper as tomarket
from okxracer.core.tapper import run_tapper as okxracer
from notpixel.core.tapper import run_tapper as notpixel
from seed.core.tapper import run_tapper as seed
from memefi.core.tapper import run_tapper as memefi
from blum.core.tapper import run_tapper as blum

APP_FUNCTIONS = {
    'coinsweeper': coinsweeper,
    'tomarket': tomarket,
    'okxracer': okxracer,
    'notpixel': notpixel,
    'seed': seed,
    'memefi': memefi,
    'blum': blum,
}

def get_session_names() -> set[str]:
    session_names = sorted(glob.glob("sessions/*.session"))
    return set(
        os.path.splitext(os.path.basename(file))[0] for file in session_names
    )

def get_tg_clients() -> list[Client]:
    session_names = get_session_names()
    tg_clients = []
    for session in Config.sessions:
        if session not in session_names:
            glogger.warning(f"Session not found: {session}")
            continue
        tg_clients.append(Client(session))

    return tg_clients

async def create_tasks(tg_clients: list[Client]) -> list[asyncio.Task]:
    tasks = []
    for tg_client in tg_clients:
        for app in tg_client.apps:
            target_function = APP_FUNCTIONS.get(app)
            if target_function is None:
                glogger.warning(f"App function not found: {app}")
                continue
            task = asyncio.create_task(target_function(tg_client=tg_client, proxy=None))
            tasks.append(task)
    return tasks
