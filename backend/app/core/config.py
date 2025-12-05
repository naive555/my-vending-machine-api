from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="")
    DATABASE_USER: str = Field(default="")
    DATABASE_PASSWORD: str = Field(default="")
    DATABASE_DB: str = Field(default="")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
