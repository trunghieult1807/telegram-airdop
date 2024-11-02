from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.api_detector_config import ApiDetectorConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    APP_NAME: str = 'coinsweeper'
    API_ID: int
    API_HASH: str


    REF_LINK: str = "https://t.me/BybitCoinsweeper_Bot?start=referredBy=5268227136"
    GAME_PLAY_EACH_ROUND: list[int] = [2, 4]
    TIME_PLAY_EACH_GAME: list[int] = [130, 180]

    ADVANCED_ANTI_DETECTION: bool = True

    DELAY_EACH_ACCOUNT: list[int] = [20, 30]

    USE_PROXY_FROM_FILE: bool = False
    
    api_detector_config: ApiDetectorConfig = ApiDetectorConfig(
        app_url = 'https://bybitcoinsweeper.com/',
        target_apis = {
            'https://api.bybitcoinsweeper.com/api',
            'auth/login',
            'auth/refresh-token',
            'games/lose',
            'games/start',
            'games/win',
        },
    )

settings = Settings()

