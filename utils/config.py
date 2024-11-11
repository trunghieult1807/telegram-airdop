from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str
    DEBUG: bool = False
    USE_TELEGRAM_NOTI: bool = False
    BOT_TOKEN: str = ''
    ERROR_CHAT_ID: str = ''
    CRITICAL_CHAT_ID: str = ''
    CHAT_LIMIT: int = 3
    CHAT_LIMIT_WINDOW: int = 60 # seconds
    

settings = Settings()

