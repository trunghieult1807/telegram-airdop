from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.api_detector_config import ApiDetectorConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    APP_NAME: str = 'seed'
    API_ID: int
    API_HASH: str

    REF_LINK: str = "t.me/seed_coin_bot/app?startapp=5268227136"

    AUTO_UPGRADE_STORAGE: bool = True
    AUTO_UPGRADE_MINING: bool = True
    AUTO_UPGRADE_HOLY: bool = True
    AUTO_CLEAR_TASKS: bool = True
    AUTO_START_HUNT: bool = True

    AUTO_SPIN: bool = True
    SPIN_PER_ROUND: list[int] = [5, 10]
    AUTO_FUSION: bool = True
    MAXIMUM_PRICE_TO_FUSION_COMMON: int = 30
    MAXIMUM_PRICE_TO_FUSION_UNCOMMON: int = 200
    MAXIMUM_PRICE_TO_FUSION_RARE: int = 800
    MAXIMUM_PRICE_TO_FUSION_EPIC: int = 3000
    MAXIMUM_PRICE_TO_FUSION_LEGENDARY: int = 20000

    AUTO_SELL_WORMS: bool = False
    QUANTITY_TO_KEEP: dict = {
        "common": {
            "quantity_to_keep": 2,
            "sale_price": 1
        },
        "uncommon": {
            "quantity_to_keep": 2,
            "sale_price": 0
        },
        "rare": {
            "quantity_to_keep": -1,
            "sale_price": 0
        },
        "epic": {
            "quantity_to_keep": -1,
            "sale_price": 0
        },
        "legendary": {
            "quantity_to_keep": -1,
            "sale_price": 0
        }
    }

    ADVANCED_ANTI_DETECTION: bool = True

    USE_PROXY_FROM_FILE: bool = False
    
    api_detector_config: ApiDetectorConfig = ApiDetectorConfig(
        app_url = 'https://cf.seeddao.org/',
        target_apis = {
            'https://alb.seeddao.org',
        },
        ignore_js_scripts = {
            'https://telegram.org/js/telegram-web-app.js',
            'https://tganalytics.xyz/index.js',
        },
        headers = {
            'accept': '*/*',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
        },
        headers_js = {
            'accept': '*/*',
            'sec-ch-ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
        }
    )

settings = Settings()


