from pydantic import BaseSettings, SecretStr, BaseModel, Field


class Settings(BaseSettings):
    BOT_TOKEN: SecretStr = Field(
        description="Токен бота",
    )
    SECRET_TOKEN: SecretStr = Field(
        description="Секретный токен для вебхука",
    )
    HOST: str = Field(
        description="Хост",
        default="0.0.0.0",
    )
    PORT: int = Field(
        description="Порт",
        default=8000
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False  # env-переменные не чувствительны к регистру


settings = Settings()