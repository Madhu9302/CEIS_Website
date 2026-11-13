from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ADMIN_EMAIL: str = "admin@codeeagle.com"
    ADMIN_PASSWORD: str = "AdminPassword123!"

    # This replaces "class Config:" for Pydantic V2
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()