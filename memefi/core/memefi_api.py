from random import randint

from aiohttp import ClientSession
from asyncio import sleep

from memefi.exceptions import InvalidProtocol
from memefi.utils.boosts import FreeBoostType, UpgradableBoostType
from memefi.utils.graphql import OperationName, Query
from memefi.utils.logger import SessionLogger


class MemeFiApi:

    GRAPHQL_URL: str = "https://api-gw-tg.memefi.club/graphql"
    _http_client: ClientSession

    def __init__(self, logger: SessionLogger) -> None:
        self.log = logger

    def set_http_client(self, http_client: ClientSession):
        self._http_client = http_client

    async def _send_request(self, request_data: dict):
        request = await self._http_client.post(url=self.GRAPHQL_URL, json=request_data)
        request.raise_for_status()
        response = await request.json()
        return response

    async def get_access_token(self, tg_web_data: dict[str]):
        for _ in range(2):
            try:
                response_json = await self._send_request(tg_web_data)

                if 'errors' in response_json:
                    raise InvalidProtocol(f'get_access_token msg: {response_json["errors"][0]["message"]}')

                access_token = response_json.get('data', {}).get('telegramUserLogin', {}).get('access_token', '')

                if not access_token:
                    await sleep(delay=5)
                    continue

                return access_token
            except Exception as error:
                self.log.error(f"❗️ Unknown error while getting Access Token: {error}")
                await sleep(delay=15)

        return ""

    async def get_profile_data(self):
        try:
            json_data = {
                'operationName': OperationName.QUERY_GAME_CONFIG,
                'query': Query.QUERY_GAME_CONFIG,
                'variables': {}
            }
            response_json = await self._send_request(json_data)

            if 'errors' in response_json:
                raise InvalidProtocol(f'get_profile_data msg: {response_json["errors"][0]["message"]}')

            profile_data = response_json['data']['telegramGameGetConfig']

            return profile_data
        except Exception as error:
            self.log.error(f"❗️Unknown error while getting Profile Data: {error}")
            await sleep(delay=9)

    async def get_telegram_me(self):
        try:
            json_data = {
                'operationName': OperationName.QueryTelegramUserMe,
                'query': Query.QueryTelegramUserMe,
                'variables': {}
            }

            response_json = await self._send_request(json_data)

            if 'errors' in response_json:
                raise InvalidProtocol(f'get_telegram_me msg: {response_json["errors"][0]["message"]}')

            me = response_json['data']['telegramUserMe']

            return me
        except Exception as error:
            self.log.error(f"❗️ Unknown error while getting Telegram Me: {error}")
            await sleep(delay=3)

            return {}

    async def wallet_check(self):
        try:
            json_data = {
                'operationName': OperationName.TelegramMemefiWallet,
                'query': Query.TelegramMemefiWallet,
                'variables': {}
            }

            response_json = await self._send_request(json_data)

            no_wallet_response = {'data': {'telegramMemefiWallet': None}}
            if response_json == no_wallet_response:
                none_wallet = "-"
                linea_wallet = none_wallet
                return linea_wallet
            else:
                linea_wallet = response_json.get('data', {}).get('telegramMemefiWallet', {}).get('walletAddress', {})
                return linea_wallet
        except Exception as error:
                self.log.error(f"❗️ Unknown error when Get Wallet: {error}")
                return None

    async def apply_boost(self, boost_type: FreeBoostType):
        try:
            json_data = {
                'operationName': OperationName.telegramGameActivateBooster,
                'query': Query.telegramGameActivateBooster,
                'variables': {
                    'boosterType': boost_type
                }
            }
            await self._send_request(json_data)
            return True
        except Exception as error:
            self.log.error(f"❗️ Unknown error while Apply {boost_type} Boost: {error}")
            await sleep(delay=9)
            return False

    async def upgrade_boost(self, boost_type: UpgradableBoostType):
        try:
            json_data = {
                'operationName': OperationName.telegramGamePurchaseUpgrade,
                'query': Query.telegramGamePurchaseUpgrade,
                'variables': {
                    'upgradeType': boost_type
                }
            }
            response_json = await self._send_request(json_data)

            if 'errors' in response_json:
                raise InvalidProtocol(f'upgrade_boost msg: {response_json["errors"][0]["message"]}')
            return True
        except Exception:
            return False

    async def set_next_boss(self):
        try:
            json_data = {
                'operationName': OperationName.telegramGameSetNextBoss,
                'query': Query.telegramGameSetNextBoss,
                'variables': {}
            }

            await self._send_request(json_data)

            return True
        except Exception as error:
            self.log.error(f"❗️Unknown error while Setting Next Boss: {error}")
            await sleep(delay=9)

            return False

    async def send_taps(self, nonce: str, taps: int):
        try:
            vector_array = []
            for tap in range(taps):
                tap = randint(1, 10)
                vector_array.append(tap)
            vector = ",".join(str(x) for x in vector_array)
            json_data = {
                'operationName': OperationName.MutationGameProcessTapsBatch,
                'query': Query.MutationGameProcessTapsBatch,
                'variables': {
                    'payload': {
                        'nonce': nonce,
                        'tapsCount': taps,
                        'vector': vector
                    },
                }
            }
            response_json = await self._send_request(json_data)
            if 'errors' in response_json:
                raise InvalidProtocol(f'send_taps msg: {response_json["errors"][0]["message"]}')

            return response_json['data']['telegramGameProcessTapsBatch']

        except Exception as error:
            self.log.error(f"❗️ Unknown error when Tapping: {error}")
            await sleep(delay=9)

    async def get_campaigns(self):
        try:
            json_data = {
                'operationName': "CampaignLists",
                'query': Query.CampaignLists,
                'variables': {}
            }

            response_json = await self._send_request(json_data)

            if 'errors' in response_json:
                self.log.error(f"Error while getting campaigns: {response_json['errors'][0]['message']}")
                return None

            campaigns = response_json.get('data', {}).get('campaignLists', {}).get('normal', [])
            return [campaign for campaign in campaigns if 'youtube' in campaign.get('description', '').lower()]

        except Exception as e:
            self.log.error(f"Unknown error while getting campaigns: {str(e)}")
            return {}

    async def verify_campaign(self, task_id: str):
        try:
            json_data = {
                'operationName': "CampaignTaskToVerification",
                'query': Query.CampaignTaskToVerification,
                'variables': {'taskConfigId': task_id}
            }

            response_json = await self._send_request(json_data)

            if 'errors' in response_json:
                self.log.error(f"Error while verifying task: {response_json['errors'][0]['message']}")
                return None

            return response_json.get('data', {}).get('campaignTaskMoveToVerificationV2')
        except Exception as e:
            self.log.error(f"Unknown error while verifying task: {str(e)}")
            return None

    async def complete_task(self, user_task_id: str, code: str = None):
        try:
            json_data = {
                'operationName': "CampaignTaskMarkAsCompleted",
                'query': Query.CampaignTaskMarkAsCompleted,
                'variables': {'userTaskId': user_task_id, 'verificationCode': str(code)} if code \
                    else  {'userTaskId': user_task_id}
            }

            response_json = await self._send_request(json_data)

            if 'errors' in response_json:
                self.log.error(f"Error while completing task: {response_json['errors'][0]['message']}")
                return None

            return response_json.get('data', {}).get('campaignTaskMarkAsCompleted')

        except Exception as e:
            self.log.error(f"Unknown error while completing task: {str(e)}")
            return None

    async def get_tasks_list(self, campaigns_id: str):
        try:
            json_data = {
                'operationName': "GetTasksList",
                'query': Query.GetTasksList,
                'variables': {'campaignId': campaigns_id}
            }

            response_json = await self._send_request(json_data)

            if 'errors' in response_json:
                self.log.error(f"Error while getting tasks: {response_json['errors'][0]['message']}")
                return None

            return response_json.get('data', {}).get('campaignTasks', [])

        except Exception as e:
            self.log.error(f"Unknown error while getting tasks: {str(e)}")
            return None

    async def get_task_by_id(self, task_id: str):
        try:
            json_data = {
                'operationName': "GetTaskById",
                'query': Query.GetTaskById,
                'variables': {'taskId': task_id}
            }

            response_json = await self._send_request(json_data)

            if 'errors' in response_json:
                self.log.error(f"Error while getting task by id: {response_json['errors'][0]['message']}")
                return None

            return response_json.get('data', {}).get('campaignTaskGetConfig')
        except Exception as e:
            self.log.error(f"Unknown error while getting task by id: {str(e)}")
            return None

    async def get_clan(self):
        try:
            json_data = {
                'operationName': OperationName.ClanMy,
                'query': Query.ClanMy,
                'variables': {}
            }

            response_json = await self._send_request(json_data)

            data = response_json['data']['clanMy']
            if data and data['id']:
                return data['id']
            else:
                return False

        except Exception as error:
            self.log.error(f"❗️Unknown error while get clan: {error}")
            await sleep(delay=9)
            return False

    async def leave_clan(self):
        try:
            json_data = {
                'operationName': OperationName.Leave,
                'query': Query.Leave,
                'variables': {}
            }

            response_json = await self._send_request(json_data)

            if response_json['data']:
                if response_json['data']['clanActionLeaveClan']:
                    return True

        except Exception as error:
            self.log.error(f"❗️Unknown error while clan leave: {error}")
            await sleep(delay=9)
            return False

    async def join_clan(self):
        try:
            json_data = {
                'operationName': OperationName.Join,
                'query': Query.Join,
                'variables': {
                    'clanId': '71886d3b-1186-452d-8ac6-dcc5081ab204'
                }
            }

            while True:
                response = await self._http_client.post(url=self.GRAPHQL_URL, json=json_data)
                response.raise_for_status()
                response_json = await response.json()
                if response_json['data']:
                    if response_json['data']['clanActionJoinClan']:
                        return True
                elif response_json['errors']:
                    await sleep(2)
                    return False

        except Exception as error:
            self.log.error(f"❗️ Unknown error while clan join: {error}")
            await sleep(delay=9)
            return False

    async def start_bot(self):
        try:
            json_data = {
                'operationName': OperationName.TapbotStart,
                'query': Query.TapbotStart,
                'variables': {}
            }

            await self._send_request(json_data)

            return True
        except Exception as error:
            self.log.error(f"❗️ Unknown error while Starting Bot: {error}")
            await sleep(delay=9)

            return False

    async def get_bot_config(self):
        try:
            json_data = {
                'operationName': OperationName.TapbotConfig,
                'query': Query.TapbotConfig,
                'variables': {}
            }

            response_json = await self._send_request(json_data)

            bot_config = response_json['data']['telegramGameTapbotGetConfig']

            return bot_config
        except Exception as error:
            self.log.error(f"❗️ Unknown error while getting Bot Config: {error}")
            await sleep(delay=9)

    async def claim_bot(self):
        try:
            json_data = {
                'operationName': OperationName.TapbotClaim,
                'query': Query.TapbotClaim,
                'variables': {}
            }

            response_json = await self._send_request(json_data)

            return {"isClaimed": False, "data": response_json['data']["telegramGameTapbotClaim"]}
        except Exception as error:
            return {"isClaimed": True, "data": None}

    async def claim_referral_bonus(self):
        try:
            json_data = {
                'operationName': OperationName.Mutation,
                'query': Query.Mutation,
                'variables': {}
            }

            await self._send_request(json_data)
            return True
        except Exception as error:
            self.log.error(f"❗️ Unknown error while Claiming Referral Bonus: {error}")
            await sleep(delay=9)
            return False

    async def play_slotmachine(self, spin_value: int):

        try:
            json_data = {
                'operationName': OperationName.SpinSlotMachine,
                'query': Query.SpinSlotMachine,
                'variables': {
                    'payload': {
                        'spinsCount': spin_value
                    }
                }
            }

            response_json = await self._send_request(json_data)
            return response_json.get('data', {}).get('slotMachineSpinV2', {})
        except Exception as error:
            self.log.error(f"❗️ Unknown error when Play Casino: {error}")
            return {}