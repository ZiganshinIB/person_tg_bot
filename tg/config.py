from pydantic import BaseSettings, SecretStr, BaseModel, Field


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr = Field(
        description="Токен бота",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False  # env-переменные не чувствительны к регистру


settings = Settings()