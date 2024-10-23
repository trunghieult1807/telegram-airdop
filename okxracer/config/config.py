from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str

    SLEEP_TIME: list[int] = [300, 500]
    START_DELAY: list[int] = [25, 55]
    MAX_COMBO_COUNT: int = 28
    AUTO_BOOST: bool = True
    AUTO_TASK: bool = True
    REF_ID: str = '61121385'
    RANDOM_PREDICTION: bool = False
    BOOSTERS: dict = {
        "Reload Fuel Tank": True,
        "Fuel Tank": True,
        "Turbo Charger": True,
    }

    USE_PROXY_FROM_FILE: bool = False


settings = Settings()
