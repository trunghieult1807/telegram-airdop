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

    USE_NEW_PAINT_METHOD: bool = False
    USE_CUSTOM_TEMPLATE: bool = True
    CUSTOM_TEMPLATE_ID: int = 6624523270
    USE_RANDOM_TEMPLATES: bool = False
    RANDOM_TEMPLATES_ID: list[int] = [6493211155, 6989019093, 917981974, 7319890725, 799818229, 1972552043, 7114665280, 5323541038, 1964161795, 5522474073,
                                      6578955397, 737065053, 347622105, 446378180, 379402843, 6914611412, 1325258259, 175225616, 2107125948, 1811879982, 5465341011, 1678134459]

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
