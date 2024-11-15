from pydantic_settings import BaseSettings, SettingsConfigDict
from utils.api_detector_config import ApiDetectorConfig


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    APP_NAME: str = 'notpixel'
    API_ID: int
    API_HASH: str

    REF_LINK: str = "https://t.me/notpixel/app?startapp=f7411517918"
    AUTO_UPGRADE_PAINT_REWARD: bool = True
    AUTO_UPGRADE_RECHARGE_SPEED:bool = True
    AUTO_UPGRADE_RECHARGE_ENERGY:bool = True
    AUTO_TASK: bool = True

    USE_PUMPKIN_BOMBS: bool = True

    USE_NEW_PAINT_METHOD: bool = True
    USE_CUSTOM_TEMPLATE: bool = False
    # CUSTOM_TEMPLATE_ID: int = 6624523270
    USE_RANDOM_TEMPLATES: bool = True
    RANDOM_TEMPLATES_ID: list[int] = [799818229, 6980731838, 5970044627, 1325258259, 1307361893, 1089170656, 6476501580, 153665413, 1311866928, 1353629816, 482706122, 1675295056, 541000485, 355876562, 249769992]

    NIGHT_MODE: bool = False
    SLEEP_TIME: list[int] = [0, 7] # your time zone

    DELAY_EACH_ACCOUNT: list[int] = [10,15]
    SLEEP_TIME_BETWEEN_EACH_ROUND: list[int] = [1000, 1500]

    ADVANCED_ANTI_DETECTION: bool = True

    USE_PROXY_FROM_FILE: bool = False

    BOT_TOKEN: str = ""
    
    api_detector_config: ApiDetectorConfig = ApiDetectorConfig(
        app_url = 'https://app.notpx.app/',
        target_apis = {
            '/users/me',
            '/mining/status',
            '/repaint/start',
            '/mining/boost/check/',
            '/mining/claim',
            '/image/template/my',
            '/image/template/',
            '/image/template/subscribe/',
            '/repaint/start',
            '/mining/task/check/',
        },
        ignore_js_scripts = {
            'https://telegram.org/js/telegram-web-app.js',
            'https://tganalytics.xyz/index.js',
            './pixi.min.js',
            './viewport.min.js',
        },
    )


settings = Settings()
