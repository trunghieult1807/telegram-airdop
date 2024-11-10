import os
from pyrogram import Client as BaseClient
from utils.config import settings
from core.agents import generate_random_user_agent
from core.config import Config


SESSION_DIR = 'sessions/'

class Client(BaseClient):
    def __init__(self, name, **kwargs):
        kwargs['api_id'] = os.getenv(f"{name.upper()}_API_ID", settings.API_ID)
        kwargs['api_hash'] = os.getenv(f"{name.upper()}_API_HASH", settings.API_HASH)
        kwargs['workdir'] = SESSION_DIR
        super().__init__(name, **kwargs)
        self.user_agent = generate_random_user_agent()
        self.apps = Config.get_session_run_apps(name)
        