import os
import glob
import asyncio
import itertools
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

from coinsweeper.core.tapper import Tapper as Coinsweeper
from okxracer.core.tapper import Tapper as Okxracer
from notpixel.core.tapper import Tapper as Notpixel
from seed.core.tapper import Tapper as Seed
from memefi.core.tapper import Tapper as Memefi
from blum.core.tapper import Tapper as Blum

APP_FUNCTIONS = {
    'coinsweeper': coinsweeper,
    'tomarket': tomarket,
    'okxracer': okxracer,
    'notpixel': notpixel,
    'seed': seed,
    'memefi': memefi,
    'blum': blum,
}

TAPPERS = {
    'coinsweeper': Coinsweeper,
    'okxracer': Okxracer,
    'notpixel': Notpixel,
    'seed': Seed,
    'memefi': Memefi,
    'blum': Blum,
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

def prepare_runners(tg_clients: list[Client]):
    runners = []
    for tg_client in tg_clients:
        for app in tg_client.apps:
            tapper_class = TAPPERS.get(app)
            if tapper_class is None:
                glogger.warning(f"App class not found: {app}")
                continue
            runners.append(tapper_class(tg_client=tg_client, multi_thread=False, proxy=None))
    return runners

async def launch(tg_clients: list[Client]) -> None:
    if Config.multi_thread:
        await asyncio.gather(*await create_tasks(tg_clients))
    else:
        runners_cycle = itertools.cycle(prepare_runners(tg_clients))
        while True:
            try:
                runner = next(runners_cycle)
                await runner.run_one_time()
            except Exception as e:
                glogger.error(f"Error: {e}")
