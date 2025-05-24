from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AUTH_SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    DATABASE_URL: str
    MODE: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
