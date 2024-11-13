from typing import Tuple, Type
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)

TOML_FILE = ['config.toml', 'config.local.toml']

class Settings(BaseSettings):
    model_config = SettingsConfigDict(toml_file=TOML_FILE, extra='allow')
    
    apps: set[str] = []
    sessions: set[str] = []
    multi_thread: bool = True
    
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
    
    def get_session_run_apps(self, session: str) -> list[str]:
        session_config = self.dict().get(session)
        if session_config is None:
            return list(self.apps)
        
        return [app for app in self.apps if session_config is None or app not in session_config['skip_app']]

Config = Settings()
