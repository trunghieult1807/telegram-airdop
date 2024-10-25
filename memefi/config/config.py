from pydantic_settings import BaseSettings, SettingsConfigDict

USER_AGENTS_FILE = "user_agents.json"
CLAN_CHECK_FILE = 'clancheck.txt'
FIRST_RUN_FILE = 'referral.txt'

class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str

    MIN_AVAILABLE_ENERGY: int = 300
    SLEEP_BY_MIN_ENERGY: int = 314

    ADD_TAPS_ON_TURBO: list[int] = [2500, 2800]

    AUTO_BUY_TAPBOT: bool = True

    AUTO_UPGRADE_TAP: bool = True
    MAX_TAP_LEVEL: int = 5
    AUTO_UPGRADE_ENERGY: bool = False
    MAX_ENERGY_LEVEL: int = 5
    AUTO_UPGRADE_CHARGE: bool = False
    MAX_CHARGE_LEVEL: int = 3

    APPLY_DAILY_ENERGY: bool = True
    APPLY_DAILY_TURBO: bool = True

    RANDOM_TAPS_COUNT: list[int] = [25, 31]
    SLEEP_BETWEEN_TAP: list[int] = [19, 36]

    USE_PROXY_FROM_FILE: bool = False
    
    REF: bool = True
    REF_ID: str = 'r_d9b87137ff'

    EMERGENCY_STOP: bool = False

    ROLL_CASINO: bool = True
    VALUE_SPIN: int = 10
    LOTTERY_INFO: bool = True

    LINEA_WALLET: bool = False
    LINEA_SHOW_BALANCE: bool = False
    LINEA_API: str = ''

    USE_RANDOM_DELAY_IN_RUN: bool = True
    RANDOM_DELAY_IN_RUN: list[int] = [3, 15]

    WATCH_VIDEO: bool = False


settings = Settings()
