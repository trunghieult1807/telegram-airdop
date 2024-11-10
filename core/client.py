import os
import json
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
        self.apps = Config.get_session_run_apps(name)
        self.session_name = name
        self.session_ua_dict = self.load_user_agents() or []
        self.user_agent = self.check_user_agent()

    
    def load_user_agents(self):
        user_agents_file_name = "user_agents.json"

        try:
            with open(user_agents_file_name, 'r') as user_agents:
                session_data = json.load(user_agents)
                if isinstance(session_data, list):
                    return session_data
        except:
            return []
    
    def save_user_agent(self):
        user_agents_file_name = "user_agents.json"

        if not any(session['session_name'] == self.session_name for session in self.session_ua_dict):
            user_agent_str = self.user_agent

            self.session_ua_dict.append({
                'session_name': self.session_name,
                'user_agent': user_agent_str})

            with open(user_agents_file_name, 'w') as user_agents:
                json.dump(self.session_ua_dict, user_agents, indent=4)

            return user_agent_str

    def check_user_agent(self):
        load = next(
            (session['user_agent'] for session in self.session_ua_dict if session['session_name'] == self.session_name),
            None)

        if load is None:
            return generate_random_user_agent()

        return load