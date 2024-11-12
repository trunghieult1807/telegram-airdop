import tomllib
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class SessionConfig(BaseModel):
    skip_app: set[str] = {}

class BotConfig(BaseSettings):
    apps: set[str] = []
    sessions: set[str] = []
    sessions_config: dict[str, SessionConfig] = Field(default_factory=dict)
    multi_thread: bool = True

    @classmethod
    def parse_toml(cls, path: str):
        with open(path, 'rb') as f:
            config_data = tomllib.load(f)
        config_data['sessions_config'] = {
            session_name: SessionConfig(**config_data[session_name])
            for session_name in config_data.get('sessions', [])
            if session_name in config_data
        }
        selected_fields = { 'apps', 'sessions', 'sessions_config', 'multi_thread' }
        config_data = { k: v for k, v in config_data.items() if k in selected_fields }
        return cls(**config_data)
    
    def get_session_run_apps(self, session: str) -> list[str]:
        return [app for app in self.apps if session not in self.sessions_config or app not in self.sessions_config[session].skip_app]

Config = BotConfig.parse_toml('config.toml')
