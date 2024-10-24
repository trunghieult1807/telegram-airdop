from aiohttp import ClientSession, ClientTimeout
from better_proxy import Proxy
from os import path

from memefi.config.config import CLAN_CHECK_FILE, FIRST_RUN_FILE


def first_check_clan():
    return not path.exists(CLAN_CHECK_FILE)

def set_first_run_check_clan():
    with open(CLAN_CHECK_FILE, 'w') as file:
        file.write('This file indicates that the script has already run once.')

def is_first_run():
    return not path.exists(FIRST_RUN_FILE)

def set_first_run():
    with open(FIRST_RUN_FILE, 'w') as file:
        file.write('https://youtu.be/dQw4w9WgXcQ')

async def check_proxy(http_client: ClientSession, proxy: Proxy) -> None:
    response = await http_client.get(url='https://api.ipify.org?format=json', timeout=ClientTimeout(5))
    ip = (await response.json()).get('ip')
    return ip
