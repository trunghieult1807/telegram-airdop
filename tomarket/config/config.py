from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str

    REF_ID: str = '0000q294'
    
    FAKE_USERAGENT: bool = True
    POINTS_COUNT: list[int] = [450, 600]
    AUTO_PLAY_GAME: bool = True
    AUTO_TASK: bool = True
    AUTO_DAILY_REWARD: bool = True
    AUTO_CLAIM_STARS: bool = True
    AUTO_CLAIM_COMBO: bool = True
    AUTO_RANK_UPGRADE: bool = True
    AUTO_RAFFLE: bool = True
    AUTO_CHANGE_NAME: bool = False
    AUTO_ADD_WALLET: bool = False

    USE_RANDOM_DELAY_IN_RUN: bool = True
    RANDOM_DELAY_IN_RUN: list[int] = [0, 15]

    USE_PROXY_FROM_FILE: bool = False
    ADVANCED_ANTI_DETECTION: bool = False
    DEBUG: bool = False


settings = Settings()
