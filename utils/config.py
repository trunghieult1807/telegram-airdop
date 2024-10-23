from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str
    DEBUG: bool = False
    USE_TELEGRAM_NOTI: bool = False
    BOT_TOKEN: str
    CHAT_ID: str
    

settings = Settings()

