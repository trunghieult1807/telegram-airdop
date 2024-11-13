from typing import Tuple, Type
from pydantic import BaseModel, Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

TOML_FILE = ['config.toml', 'config.local.toml']


class SessionConfig(BaseModel):
    apps: set[str] = None
    skip_app: set[str] = {}

class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=TOML_FILE, extra='allow')
    
    apps: set[str] = []
    sessions: set[str] = []
    multi_thread: bool = True
    sessions_config: dict[str, SessionConfig] = Field(default_factory=dict)
    
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls),)
    
    def __init__(self, **data):
        super().__init__(**data)
        self.sessions_config = self.build_sessions_config()
        
    def build_sessions_config(self):
        config_dict = self.dict()
        return { session: SessionConfig(**config_dict.get(session)) for session in self.sessions }
    
    def get_session_run_apps(self, session: str) -> list[str]:
        if session not in self.sessions:
            return []
        
        session_config = self.sessions_config.get(session)
        apps = self.apps if session_config.apps is None else session_config.apps
        
        return list(apps.difference(session_config.skip_app))

Config = Settings()
