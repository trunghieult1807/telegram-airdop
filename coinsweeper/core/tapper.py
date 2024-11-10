import asyncio
import random
import traceback
from itertools import cycle
from time import time
from urllib.parse import unquote

import hmac
import hashlib
import aiohttp
from datetime import datetime

import pytz
from better_proxy import Proxy
from core.client import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw import functions
from pyrogram.raw.functions.messages import RequestWebView
from coinsweeper.config import settings

from coinsweeper.utils import logger
from exceptions import InvalidSession
from random import randint
import math
import sys
from coinsweeper.core.query import Tapper as QueryTapper


def value(i):
    return sum(ord(o) for o in list(i)) / 1e5


def calc(i, s, a, o, d, g):
    st = (10 * i + max(0, 1200 - 10 * s) + 2000) * (1 + o / a) / 10
    return math.floor(st) + value(g)


# mr = calc(45, 150, 54, 9, True, "17d26c4f-a453-4e29-b9bd-89c79a20d312")


class Tapper(QueryTapper):
    def __init__(self, tg_client: Client, multi_thread: bool, proxy: str | None):
        super().__init__(query='', session_name=tg_client.name, multi_thread=multi_thread, proxy=proxy)
        self.tg_client = tg_client
        
    async def get_tg_web_data(self) -> str:
        try:
            if settings.REF_LINK == "":
                ref_param = "referredBy=5268227136"
            else:
                ref_param =settings.REF_LINK.split("=")[1] + "=" + settings.REF_LINK.split("=")[2]
        except:
            logger.error(f"{self.session_name} | Ref link invaild please check again !")
            sys.exit()
        # print(ref_param)
        self.ref_id = settings.REF_LINK.split('=')[2] if settings.REF_LINK != "" else "5268227136"
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
                    start_command_found = False
                    async for message in self.tg_client.get_chat_history('BybitCoinsweeper_Bot'):
                        if (message.text and message.text.startswith('/start')) or (
                                message.caption and message.caption.startswith('/start')):
                            start_command_found = True
                            break
                    if not start_command_found:
                        peer = await self.tg_client.resolve_peer('BybitCoinsweeper_Bot')
                        await self.tg_client.invoke(
                            functions.messages.StartBot(
                                bot=peer,
                                peer=peer,
                                start_param=ref_param,
                                random_id=randint(1, 9999999),
                            )
                        )
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.session_name)

            while True:
                try:
                    peer = await self.tg_client.resolve_peer('BybitCoinsweeper_Bot')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"<light-yellow>{self.session_name}</light-yellow> | FloodWait {fl}")
                    logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Sleep {fls}s")

                    await asyncio.sleep(fls + 3)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=peer,
                bot=peer,
                platform='android',
                from_bot_menu=False,
                url="https://bybitcoinsweeper.com",
                start_param=ref_param
            ))

            auth_url = web_view.url
            # print(auth_url)
            tg_web_data = unquote(
                string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))

            self.user_id = tg_web_data.split('"id":')[1].split(',"first_name"')[0]
            self.first_name = tg_web_data.split('"first_name":"')[1].split('","last_name"')[0]
            self.last_name = tg_web_data.split('"last_name":"')[1].split('","username"')[0]

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

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
