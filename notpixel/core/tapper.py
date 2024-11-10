import asyncio
import json
import random
from itertools import cycle
from urllib.parse import unquote

from better_proxy import Proxy
from core.client import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.types import InputBotAppShortName
from pyrogram.raw.functions.messages import RequestAppWebView
from notpixel.config import settings
from notpixel.core.query import Tapper as QueryTapper
from exceptions import InvalidSession
from notpixel.utils import logger
from random import randint
import urllib3
import base64
import os
import sys


def generate_websocket_key():
    random_bytes = os.urandom(16)
    websocket_key = base64.b64encode(random_bytes).decode('utf-8')
    return websocket_key


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_GAME_ENDPOINT = "https://notpx.app/api/v1"


class Tapper(QueryTapper):
    def __init__(self, tg_client: Client, multi_thread: bool, proxy: str | None):
        super().__init__(query='', session_name=tg_client.name, multi_thread=multi_thread, proxy=proxy)
        self.tg_client = tg_client

    async def get_tg_web_data(self) -> str:
        try:
            if settings.REF_LINK == "":
                ref_param = "f7411517918"
            else:
                ref_param = settings.REF_LINK.split("=")[1]
        except:
            logger.error(f"{self.session_name} | Ref link invaild please check again !")
            sys.exit()
        actual = random.choices([self.my_ref, self.clb_ref, ref_param], weights=[20, 10, 70])  # edit this line if you don't want to support me
        if self.proxy:
            proxy = Proxy.from_str(self.proxy)
            proxy_dict = dict(
                scheme=proxy.protocol,
                hostname=proxy.host,
                port=proxy.port,
                username=proxy.login,
                password=proxy.password
            )
        else:
            proxy_dict = None

        self.tg_client.proxy = proxy_dict
        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('notpixel')
                    break
                except FloodWait as fl:

                    logger.warning(f"<light-yellow>{self.session_name}</light-yellow> | FloodWait {fl}")
                    async for dialog in self.tg_client.get_dialogs():
                        if dialog.chat and dialog.chat.username and dialog.chat.username == "notpixel":
                            break

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name="app"),
                platform='android',
                write_allowed=True,
                start_param=actual[0]
            ))

            auth_url = web_view.url

            tg_web_data = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

            tg_web_data_decoded = unquote(unquote(tg_web_data))
            tg_web_data_json = tg_web_data_decoded.split('user=')[1].split('&chat_instance')[0]
            user_data = json.loads(tg_web_data_json)
            self.user_id = user_data['id']

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return tg_web_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            logger.error(f"<light-yellow>{self.session_name}</light-yellow> | Unknown error during Authorization: "
                         f"{error}")
            await asyncio.sleep(delay=3)


async def run_tapper(tg_client: Client, proxy: str | None):
    try:
        sleep_ = randint(1, 15)
        logger.info(f"{tg_client.name} | start after {sleep_}s")
        await asyncio.sleep(sleep_)
        await Tapper(tg_client=tg_client, multi_thread=True, proxy=proxy).run()
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")


async def run_tapper1(tg_clients: list[Client], proxies):
    proxies_cycle = cycle(proxies) if proxies else None
    while True:
        for tg_client in tg_clients:
            try:
                proxy = next(proxies_cycle) if proxies_cycle else None
                await Tapper(tg_client=tg_client, multi_thread=False, proxy=proxy).run()
            except InvalidSession:
                logger.error(f"{tg_client.name} | Invalid Session")

            sleep_ = randint(settings.DELAY_EACH_ACCOUNT[0], settings.DELAY_EACH_ACCOUNT[1])
            logger.info(f"Sleep {sleep_}s...")
            await asyncio.sleep(sleep_)

        sleep_ = randint(settings.SLEEP_TIME_BETWEEN_EACH_ROUND[0], settings.SLEEP_TIME_BETWEEN_EACH_ROUND[1])
        logger.info(f"<red>Sleep {sleep_}s...</red>")
        await asyncio.sleep(sleep_)