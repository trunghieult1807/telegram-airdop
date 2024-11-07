import asyncio
import random
from time import time
from random import randint
from urllib.parse import unquote
import json

import aiohttp
from aiocfscrape import CloudflareScraper
from aiohttp_proxy import ProxyConnector
from better_proxy import Proxy
from pyrogram import Client
from pyrogram.errors import Unauthorized, UserDeactivated, AuthKeyUnregistered
from pyrogram.raw.functions.messages import RequestWebView
from datetime import datetime, timezone
from dateutil import parser

from memefi.config import settings
from memefi.config.config import USER_AGENTS_FILE
from memefi.utils.checkers import first_check_clan, set_first_run_check_clan, is_first_run, set_first_run, check_proxy
from memefi.utils.graphql import Query, OperationName
from memefi.utils.boosts import FreeBoostType, UpgradableBoostType
from memefi.core.headers import headers
from memefi.core.agents import generate_random_user_agent

from memefi.core.TLS import TLSv1_3_BYPASS
from memefi.exceptions import InvalidSession, InvalidProtocol
from memefi.utils.codes import VideoCodes
from memefi.core.memefi_api import MemeFiApi
from memefi.utils.logger import SessionLogger

from utils.time_list import TimedList


class Tapper:
    def __init__(self, tg_client: Client, logger: SessionLogger):
        self.tg_client = tg_client
        self.video_codes = VideoCodes()
        self.log = logger
        self._api = MemeFiApi(logger=logger)
        self._last_update_codes_timestamp = 0

        self.session_ug_dict = self.load_user_agents() or []
        headers['User-Agent'] = self.check_user_agent()

    def save_user_agent(self):

        if not any(session['session_name'] == self.tg_client.name for session in self.session_ug_dict):
            user_agent_str = generate_random_user_agent()

            self.session_ug_dict.append({
                'session_name': self.tg_client.name,
                'user_agent': user_agent_str})

            with open(USER_AGENTS_FILE, 'w') as user_agents:
                json.dump(self.session_ug_dict, user_agents, indent=4)

            self.log.info("User agent saved successfully")

            return user_agent_str

    def load_user_agents(self):
        try:
            with open(USER_AGENTS_FILE, 'r') as user_agents:
                session_data = json.load(user_agents)
                if isinstance(session_data, list):
                    return session_data

        except FileNotFoundError:
            self.log.warning("User agents file not found, creating...")

        except json.JSONDecodeError:
            self.log.warning("User agents file is empty or corrupted.")

        return []

    def check_user_agent(self):
        load = next(
            (session['user_agent'] for session in self.session_ug_dict if session['session_name'] == self.tg_client.name),
            None)

        if load is None:
            return self.save_user_agent()

        return load

    async def get_tg_web_data(self, proxy: str = None):
        if proxy:
            proxy = Proxy.from_str(proxy)
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

        # pupa = '/start '
        # i = 'r_bc7a351b1a'
        # lupa = f"'{settings.REF_ID}'"
        # str(lupazapupu) = pupa + i
        # str(pupazalupu) = pupa + lupa

        pupa = '/start r_d9b87137ff'
        lupa = f'/start {settings.REF_ID}'

        my_friends = [pupa, lupa]

        random_friends = random.choice(my_friends)

        try:
            if not self.tg_client.is_connected:
                try:
                    await self.tg_client.connect()
                    if is_first_run() and settings.REF and settings.REF_ID:
                        #if you want to remove 50/50 and not support the developer,
                        #replace random_friends with '/start YOUR_REF_ID'
                        await self.tg_client.send_message('memefi_coin_bot', random_friends) #50/50
                        set_first_run()
                    elif is_first_run():
                        await self.tg_client.send_message('memefi_coin_bot', pupa)
                        set_first_run()
                except (Unauthorized, UserDeactivated, AuthKeyUnregistered):
                    raise InvalidSession(self.tg_client.name)

            web_view = await self.tg_client.invoke(RequestWebView(
                peer=await self.tg_client.resolve_peer('memefi_coin_bot'),
                bot=await self.tg_client.resolve_peer('memefi_coin_bot'),
                platform='android',
                from_bot_menu=False,
                url='https://tg-app.memefi.club/game'
            ))

            auth_url = web_view.url
            tg_web_data = unquote(
                string=unquote(
                    string=auth_url.split('tgWebAppData=', maxsplit=1)[1].split('&tgWebAppVersion', maxsplit=1)[0]))

            query_id = tg_web_data.split('query_id=', maxsplit=1)[1].split('&user', maxsplit=1)[0]
            user_data = tg_web_data.split('user=', maxsplit=1)[1].split('&auth_date', maxsplit=1)[0]
            auth_date = tg_web_data.split('auth_date=', maxsplit=1)[1].split('&hash', maxsplit=1)[0]
            hash_ = tg_web_data.split('hash=', maxsplit=1)[1]

            me = await self.tg_client.get_me()

            json_data = {
                'operationName': OperationName.MutationTelegramUserLogin,
                'variables': {
                    'webAppData': {
                        'auth_date': int(auth_date),
                        'hash': hash_,
                        'query_id': query_id,
                        'checkDataString': f'auth_date={auth_date}\nquery_id={query_id}\nuser={user_data}',
                        'user': {
                            'id': me.id,
                            'allows_write_to_pm': True,
                            'first_name': me.first_name,
                            'last_name': me.last_name if me.last_name else '',
                            'username': me.username if me.username else '',
                            'language_code': me.language_code if me.language_code else 'en',
                        },
                    },
                },
                'query': Query.MutationTelegramUserLogin,
            }

            if self.tg_client.is_connected:
                await self.tg_client.disconnect()

            return json_data

        except InvalidSession as error:
            raise error

        except Exception as error:
            self.log.error(f"❗️ Unknown error during Authorization: {error}")
            await asyncio.sleep(delay=5)



    async def get_linea_wallet_balance(self, http_client: aiohttp.ClientSession, linea_wallet: str):
        try:
            api_key = settings.LINEA_API
            api_url = (f"https://api.lineascan.build/api?module=account&action=balance&address="
                       f"{linea_wallet}&tag=latest&apikey={api_key}")

            async with http_client.get(api_url) as response:
                data = await response.json()
                if data['status'] == '1' and data['message'] == 'OK':
                    balance_wei = int(data['result'])
                    balance_eth = float((balance_wei / 1e18))
                    return balance_eth
                else:
                    if linea_wallet == '-':
                        balance_eth = '-'
                        return balance_eth
                    else:
                        self.log.warning(f"Failed to retrieve Linea wallet balance: {data['message']}")
                        return None
        except Exception as error:
            self.log.error(f"Error getting Linea wallet balance: {error}")
            return None

    async def get_eth_price(self, http_client: aiohttp.ClientSession, balance_eth: str):
        try:
            if balance_eth == '-':
                return balance_eth
            else:
                api_url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=ethereum"

                async with http_client.get(api_url) as response:
                    data = await response.json()
                    if response.status == 200:
                        eth_current_price = int(float(data[0]['current_price']) // 1)
                        eth_price = round((eth_current_price * float(balance_eth)), 2)
                        return eth_price
                    else:
                        self.log.warning(f"Failed to retrieve ETH price: {response.status} code")
                        return None
        except Exception as error:
            self.log.error(f"Error getting ETH price: {error}")
            return None

    async def watch_videos(self):
        if self._last_update_codes_timestamp == self.video_codes.get_last_update_timestamp() + 1:
            return

        self._last_update_codes_timestamp = self.video_codes.get_last_update_timestamp() + 1

        campaigns = await self._api.get_campaigns()
        if campaigns is None:
            self.log.error("Campaigns list is None")
            return

        if not campaigns:
            return

        campaigns_counter = 0
        for campaign in campaigns:
            campaigns_counter += 1
            await asyncio.sleep(delay=1)
            tasks_list: list = await self._api.get_tasks_list(campaigns_id=campaign['id'])
            for task in tasks_list:
                await asyncio.sleep(delay=randint(1, 3))
                # await asyncio.sleep(delay=randint(5, 15))
                index = f"{campaigns_counter}/{len(campaigns)}"
                self.log.info(f"Video {index}: <r>{task['name']}</r> | Status: <y>{task['status']}</y>")

                if task['status'] != 'Verification':
                    task = await self._api.verify_campaign(task_id=task['id'])
                    self.log.info(f"Video: <r>{task['name']}</r> | Start verifying")

                delta_time = parser.isoparse(task['verificationAvailableAt']).timestamp() - \
                             datetime.now(timezone.utc).timestamp()

                if task['status'] == 'Verification' and delta_time > 0:
                    count_sec_need_wait = delta_time + randint(5, 15)
                    self.log.info(f"Video: <r>{task['name']}</r> | Sleep: {int(count_sec_need_wait)}s.")
                    continue
                    await asyncio.sleep(delay=count_sec_need_wait)

                if task['taskVerificationType'] == "SecretCode":
                    code = self.video_codes.get_video_code(task)
                    if not code:
                        self.log.warning(f"<r>Code not found</r> | ID: <y>{task['id']}</y> ({task['link']})")
                        continue
                    complete_task = await self._api.complete_task(user_task_id=task['userTaskId'], code=code)
                    if not complete_task:
                        self.log.warning(f"<r>Code incorrect: {code}</r> | ID: <y>{task['id']}</y> ({task['link']})")
                        self.video_codes.mark_code_as_incorrect(task)
                    else:
                        self.video_codes.mark_code_as_correct(task, code)
                else:
                    complete_task = await self._api.complete_task(user_task_id=task['userTaskId'])
                message = f"<g>Complete</g>" if complete_task \
                    else f"<r>Error from complete_task method.</r>"
                self.log.info(f"Video: <r>{task['name']}</r> | Status: {message}")


    async def update_authorization(self, http_client, proxy) -> bool:
        http_client.headers.pop("Authorization", None)

        tg_web_data = await self.get_tg_web_data(proxy=proxy)

        if not tg_web_data:
            self.log.info(f"Log out!")
            raise Exception("Account is not authorized")

        access_token = await self._api.get_access_token(tg_web_data=tg_web_data)

        if not access_token:
            return False

        http_client.headers["Authorization"] = f"Bearer {access_token}"

        await self._api.get_telegram_me()
        return True

    async def run(self, proxy: str | None):
        access_token_created_time = 0
        turbo_time = 0
        active_turbo = False

        ssl_context = TLSv1_3_BYPASS.create_ssl_context()
        conn = ProxyConnector().from_url(url=proxy, rdns=True, ssl=ssl_context) if proxy \
            else aiohttp.TCPConnector(ssl=ssl_context)

        async with CloudflareScraper(headers=headers, connector=conn) as http_client:
            if proxy:
                try:
                    ip = await check_proxy(http_client=http_client, proxy=proxy)
                    self.log.info(f"Proxy IP: {ip}")
                except Exception as error:
                    self.log.error(f"Proxy: {proxy} | Error: {error}")

            self._api.set_http_client(http_client=http_client)

            while True:
                is_no_balance = False
                try:
                    if time() - access_token_created_time >= 5400:
                        is_success = await self.update_authorization(http_client=http_client, proxy=proxy)
                        if not is_success:
                            await asyncio.sleep(delay=5)
                            continue
                        access_token_created_time = time()

                    profile_data = await self._api.get_profile_data()

                    if not profile_data:
                        await asyncio.sleep(delay=5)
                        continue

                    balance = profile_data.get('coinsAmount', 0)
                    nonce = profile_data.get('nonce', '')
                    current_boss = profile_data['currentBoss']
                    current_boss_level = current_boss['level']
                    boss_max_health = current_boss['maxHealth']
                    boss_current_health = current_boss['currentHealth']
                    spins = profile_data.get('spinEnergyTotal', 0)

                    self.log.info(f"Current boss level: <m>{current_boss_level}</m> | "
                                f"Boss health: <e>{boss_current_health}</e> out of <r>{boss_max_health}</r> | "
                                f"Balance: <c>{balance}</c> | Spins: <le>{spins}</le>")

                    if settings.USE_RANDOM_DELAY_IN_RUN:
                        random_delay = random.randint(settings.RANDOM_DELAY_IN_RUN[0],
                                                      settings.RANDOM_DELAY_IN_RUN[1])
                        self.log.info(f"Bot will start in <y>{random_delay}s</y>")
                        await asyncio.sleep(random_delay)

                    if settings.LINEA_WALLET is True:
                        linea_wallet = await self._api.wallet_check()
                        self.log.info(f"💳 Linea wallet address: <y>{linea_wallet}</y>")
                        if settings.LINEA_SHOW_BALANCE:
                            if settings.LINEA_API != '':
                                balance_eth = await self.get_linea_wallet_balance(http_client=http_client,
                                                                                  linea_wallet=linea_wallet)
                                eth_price = await self.get_eth_price(http_client=http_client,
                                                                     balance_eth=balance_eth)
                                self.log.info(f"ETH Balance: <g>{balance_eth}</g> | "
                                            f"USD Balance: <e>{eth_price}</e>")
                            elif settings.LINEA_API == '':
                                self.log.info(f""
                                            f"💵 LINEA_API must be specified to show the balance")
                                await asyncio.sleep(delay=3)

                    if boss_current_health == 0:
                        self.log.info(f"👉 Setting next boss: <m>{current_boss_level + 1}</m> lvl")
                        self.log.info(f"😴 Sleep 10s")
                        await asyncio.sleep(delay=10)

                        status = await self._api.set_next_boss()
                        if status is True:
                            self.log.success(f"✅ Successful setting next boss: <m>{current_boss_level + 1}</m>")

                    if settings.WATCH_VIDEO:
                       await self.watch_videos()

                    if settings.ROLL_CASINO:
                        while spins > settings.VALUE_SPIN:
                            await asyncio.sleep(delay=2)
                            play_data = await self._api.play_slotmachine(spin_value=settings.VALUE_SPIN)
                            reward_amount = play_data.get('spinResults', [{}])[0].get('rewardAmount', 0)
                            reward_type = play_data.get('spinResults', [{}])[0].get('rewardType', 'NO')
                            spins = play_data.get('gameConfig', {}).get('spinEnergyTotal', 0)
                            balance = play_data.get('gameConfig', {}).get('coinsAmount', 0)
                            if play_data.get('ethLotteryConfig', {}) is None:
                                eth_lottery_status = '-'
                                eth_lottery_ticket = '-'
                            else:
                                eth_lottery_status = play_data.get('ethLotteryConfig', {}).get('isCompleted', 0)
                                eth_lottery_ticket = play_data.get('ethLotteryConfig', {}).get('ticketNumber', 0)
                            self.log.info(f"🎰 Casino game | "
                                        f"Balance: <lc>{balance:,}</lc> (<lg>+{reward_amount:,}</lg> "
                                        f"<lm>{reward_type}</lm>) "
                                        f"| Spins: <le>{spins:,}</le> ")
                            if settings.LOTTERY_INFO:
                                self.log.info(f"🎟 ETH Lottery status: {eth_lottery_status} |"
                                            f" 🎫 Ticket number: <yellow>{eth_lottery_ticket}</yellow>")
                            await asyncio.sleep(delay=5)

                    taps = randint(a=settings.RANDOM_TAPS_COUNT[0], b=settings.RANDOM_TAPS_COUNT[1])
                    if taps > boss_current_health:
                        taps = boss_max_health - boss_current_health - 10
                        return taps
                    bot_config = await self._api.get_bot_config()
                    telegram_me = await self._api.get_telegram_me()

                    available_energy = profile_data['currentEnergy']
                    need_energy = taps * profile_data['weaponLevel']

                    if first_check_clan():
                        clan = await self._api.get_clan()
                        set_first_run_check_clan()
                        await asyncio.sleep(1)
                        if clan is not False and clan != '71886d3b-1186-452d-8ac6-dcc5081ab204':
                            await asyncio.sleep(1)
                            clan_leave = await self._api.leave_clan()
                            if clan_leave is True:
                                await asyncio.sleep(1)
                                clan_join = await self._api.join_clan()
                                if clan_join is True:
                                    continue
                                elif clan_join is False:
                                    await asyncio.sleep(1)
                                    continue
                            elif clan_leave is False:
                                continue
                        elif clan == '71886d3b-1186-452d-8ac6-dcc5081ab204':
                            continue
                        else:
                            clan_join = await self._api.join_clan()
                            if clan_join is True:
                                continue
                            elif clan_join is False:
                                await asyncio.sleep(1)
                                continue

                    if telegram_me['isReferralInitialJoinBonusAvailable'] is True:
                        await self._api.claim_referral_bonus()
                        self.log.info(f"🔥Referral bonus was claimed")

                    if bot_config['isPurchased'] is False and settings.AUTO_BUY_TAPBOT is True:
                        await self._api.upgrade_boost(boost_type=UpgradableBoostType.TAPBOT)
                        self.log.info(f"👉 Tapbot was purchased - 😴 Sleep 7s")
                        await asyncio.sleep(delay=9)
                        bot_config = await self._api.get_bot_config()

                    if bot_config['isPurchased'] is True:
                        if bot_config['usedAttempts'] < bot_config['totalAttempts'] and not bot_config['endsAt']:
                            await self._api.start_bot()
                            bot_config = await self._api.get_bot_config()
                            self.log.info(f"👉 Tapbot is started")

                        else:
                            claim_result = await self._api.claim_bot()
                            if claim_result['isClaimed'] == False and claim_result['data']:
                                self.log.info(f"👉 Tapbot was claimed - 😴 Sleep 7s before starting again")
                                await asyncio.sleep(delay=9)
                                bot_config = claim_result['data']
                                await asyncio.sleep(delay=5)

                                if bot_config['usedAttempts'] < bot_config['totalAttempts']:
                                    await self._api.start_bot()
                                    self.log.info(f"👉 Tapbot is started - 😴 Sleep 7s")
                                    await asyncio.sleep(delay=9)
                                    bot_config = await self._api.get_bot_config()

                    if active_turbo:
                        taps += randint(a=settings.ADD_TAPS_ON_TURBO[0], b=settings.ADD_TAPS_ON_TURBO[1])
                        if taps > boss_current_health:
                            taps = boss_max_health - boss_current_health - 10
                            return taps

                        need_energy = 0

                        if time() - turbo_time > 10:
                            active_turbo = False
                            turbo_time = 0

                    if need_energy > available_energy or available_energy - need_energy < settings.MIN_AVAILABLE_ENERGY:
                        self.log.warning(f"Need more energy ({available_energy}/{need_energy}, min:"
                                       f" {settings.MIN_AVAILABLE_ENERGY}) for {taps} taps")

                        sleep_between_clicks = randint(a=settings.SLEEP_BETWEEN_TAP[0], b=settings.SLEEP_BETWEEN_TAP[1])
                        self.log.info(f"Sleep {sleep_between_clicks}s")
                        await asyncio.sleep(delay=sleep_between_clicks)
                        # update profile data
                        profile_data = await self._api.get_profile_data()
                        continue

                    profile_data = await self._api.send_taps(nonce=nonce, taps=taps)

                    if not profile_data:
                        continue

                    available_energy = profile_data['currentEnergy']
                    new_balance = profile_data['coinsAmount']

                    free_boosts = profile_data['freeBoosts']
                    turbo_boost_count = free_boosts['currentTurboAmount']
                    energy_boost_count = free_boosts['currentRefillEnergyAmount']

                    next_tap_level = profile_data['weaponLevel'] + 1
                    next_energy_level = profile_data['energyLimitLevel'] + 1
                    next_charge_level = profile_data['energyRechargeLevel'] + 1

                    nonce = profile_data['nonce']

                    current_boss = profile_data['currentBoss']
                    current_boss_level = current_boss['level']
                    boss_current_health = current_boss['currentHealth']

                    if boss_current_health <= 0:
                        self.log.info(f"👉 Setting next boss: <m>{current_boss_level + 1}</m> lvl")
                        self.log.info(f"😴 Sleep 10s")
                        await asyncio.sleep(delay=10)

                        status = await self._api.set_next_boss()
                        if status is True:
                            self.log.success(f"✅ Successful setting next boss: <m>{current_boss_level + 1}</m>")

                    if not active_turbo:
                        taps = 100
                    taps_status = await self._api.send_taps(nonce=nonce, taps=taps)
                    taps_new_balance = taps_status['coinsAmount']
                    calc_taps = taps_new_balance - balance
                    if calc_taps > 0:
                        self.log.success(f"✅ Successful tapped! 🔨 | 👉 Current energy: {available_energy} "
                            f"| ⚡️ Minimum energy limit: {settings.MIN_AVAILABLE_ENERGY} | "
                            f"Balance: <c>{taps_new_balance}</c> (<g>+{calc_taps} 😊</g>) | "
                            f"Boss health: <e>{boss_current_health}</e>")
                        balance = new_balance
                    else:
                        self.log.info(f"❌ Failed tapped! 🔨 | Balance: <c>{taps_new_balance}</c> "
                            f"(<g>No coin added 😥</g>) | 👉 Current energy: {available_energy} | "
                            f"⚡️ Minimum energy limit: {settings.MIN_AVAILABLE_ENERGY} | "
                            f"Boss health: <e>{boss_current_health}</e>")
                        balance = new_balance
                        self.log.warning(f"❌ MemeFi server error 500")
                        self.log.info(f"😴 Sleep 30s")
                        await asyncio.sleep(delay=30)
                        is_no_balance = True

                    if active_turbo is False:
                        if (energy_boost_count > 0
                                and available_energy < settings.MIN_AVAILABLE_ENERGY
                                and settings.APPLY_DAILY_ENERGY is True
                                and available_energy - need_energy < settings.MIN_AVAILABLE_ENERGY):
                            self.log.info(f"😴 Sleep 7s before activating the daily energy boost")
                            await asyncio.sleep(delay=7)

                            status = await self._api.apply_boost(boost_type=FreeBoostType.ENERGY)
                            if status is True:
                                self.log.success(f"👉 Energy boost applied")

                                await asyncio.sleep(delay=3)

                            continue

                        if turbo_boost_count > 0 and settings.APPLY_DAILY_TURBO is True:
                            self.log.info(f"😴 Sleep 10s before activating the daily turbo boost")
                            await asyncio.sleep(delay=10)

                            status = await self._api.apply_boost(boost_type=FreeBoostType.TURBO)
                            if status is True:
                                self.log.success(f"👉 Turbo boost applied")

                                await asyncio.sleep(delay=1)

                                active_turbo = True
                                turbo_time = time()

                            continue

                        if settings.AUTO_UPGRADE_TAP is True and next_tap_level <= settings.MAX_TAP_LEVEL:
                            need_balance = 1000 * (2 ** (next_tap_level - 1))
                            if balance > need_balance:
                                status = await self._api.upgrade_boost(boost_type=UpgradableBoostType.TAP)
                                if status is True:
                                    self.log.success(f"Tap upgraded to {next_tap_level} lvl")

                                    await asyncio.sleep(delay=1)
                            else:
                                self.log.info(f"Need more gold for upgrade tap to {next_tap_level}"
                                            f" lvl ({balance}/{need_balance})")

                        if settings.AUTO_UPGRADE_ENERGY is True and next_energy_level <= settings.MAX_ENERGY_LEVEL:
                            need_balance = 1000 * (2 ** (next_energy_level - 1))
                            if balance > need_balance:
                                status = await self._api.upgrade_boost(boost_type=UpgradableBoostType.ENERGY)
                                if status is True:
                                    self.log.success(f"Energy upgraded to {next_energy_level} lvl")

                                    await asyncio.sleep(delay=1)
                            else:
                                self.log.warning(f"Need more gold for upgrade energy to {next_energy_level} "
                                    f"lvl ({balance}/{need_balance})"
                               )


                        if settings.AUTO_UPGRADE_CHARGE is True and next_charge_level <= settings.MAX_CHARGE_LEVEL:
                            need_balance = 1000 * (2 ** (next_charge_level - 1))

                            if balance > need_balance:
                                status = await self._api.upgrade_boost(boost_type=UpgradableBoostType.CHARGE)
                                if status is True:
                                    self.log.success(f"Charge upgraded to {next_charge_level} lvl")

                                    await asyncio.sleep(delay=1)
                            else:
                                self.log.warning(f"Need more gold for upgrade charge to {next_energy_level} "
                                    f"lvl ({balance}/{need_balance})")


                        if available_energy < settings.MIN_AVAILABLE_ENERGY:
                            self.log.info(f"👉 Minimum energy reached: {available_energy}")
                            self.log.info(f"😴 Sleep {settings.SLEEP_BY_MIN_ENERGY}s")

                            await asyncio.sleep(delay=settings.SLEEP_BY_MIN_ENERGY)

                            continue

                except InvalidSession as error:
                    raise error

                except Exception as error:
                    self.log.error(f"❗️Unknown error: {type(error).__name__} {error}. 😴 Wait 1h")
                    await asyncio.sleep(delay=3600)

                else:
                    sleep_between_clicks = randint(a=settings.SLEEP_BETWEEN_TAP[0], b=settings.SLEEP_BETWEEN_TAP[1])

                    if active_turbo is True:
                        sleep_between_clicks = 50
                    elif is_no_balance is True:
                        sleep_between_clicks = 700

                    self.log.info(f"😴 Sleep {sleep_between_clicks}s")
                    await asyncio.sleep(delay=sleep_between_clicks)


async def run_tapper(tg_client: Client, proxy: str | None):
    session_logger = SessionLogger(tg_client.name)
    try:
        await Tapper(tg_client=tg_client, logger=session_logger).run(proxy=proxy)
    except InvalidSession:
        session_logger.error(f"❗️Invalid Session")
    except InvalidProtocol as error:
        session_logger.error(f"❗️Invalid protocol detected at {error}")