from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
