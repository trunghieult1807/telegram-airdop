import asyncio
import random
from datetime import datetime, timezone
from urllib.parse import unquote

import json
from better_proxy import Proxy
from core.client import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered, FloodWait
from pyrogram.raw.types import InputBotAppShortName
from pyrogram.raw.functions.messages import RequestAppWebView
from seed.config import settings
from seed.core.query import Tapper as QueryTapper
from seed.utils import logger
from exceptions import InvalidSession
from random import randint


class Tapper(QueryTapper):
    def __init__(self, tg_client: Client, proxy: str | None):
        super().__init__(Query='', session_name=tg_client.name, user_agent=tg_client.user_agent, proxy=proxy)
        self.tg_client = tg_client        
        
    async def get_tg_web_data(self) -> str:
        if settings.REF_LINK == '':
            ref_ = "t.me/seed_coin_bot/app?startapp=5268227136"
        else:
            ref_ = settings.REF_LINK
        ref__ = ref_.split('=')[1]
        actual = random.choices([self.my_ref, ref__], weights=[30, 70])
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
                    peer = await self.tg_client.resolve_peer('seed_coin_bot')
                    break
                except FloodWait as fl:
                    fls = fl.value

                    logger.warning(f"<light-yellow>{self.session_name}</light-yellow> | FloodWait {fl}")
                    logger.info(f"<light-yellow>{self.session_name}</light-yellow> | Sleep {fls}s")

                    await asyncio.sleep(fls + 3)

            web_view = await self.tg_client.invoke(RequestAppWebView(
                peer=peer,
                app=InputBotAppShortName(bot_id=peer, short_name="app"),
                platform='android',
                write_allowed=True,
                start_param=actual[0]
            ))

            auth_url = web_view.url
            # print(auth_url)
            tg_web_data = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])

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
        sleep_ = randint(1, 25)
        logger.info(f"Wait {sleep_}s")
        await asyncio.sleep(sleep_)
        await Tapper(tg_client=tg_client, proxy=proxy).run()
    except InvalidSession:
        logger.error(f"{tg_client.name} | Invalid Session")
