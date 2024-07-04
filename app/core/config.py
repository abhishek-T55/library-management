import logging
from pydantic_settings import BaseSettings
from pydantic import AnyUrl
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).parent

log = logging.getLogger("uvicorn")

class DatabaseConfig(BaseSettings):
    url: AnyUrl | str


class RedisConfig(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    password: str | None = None


class RabbitMQConfig(BaseSettings):
    pass


class Config(BaseSettings):
    debug: bool = True

    redis: RedisConfig = RedisConfig()
    database: DatabaseConfig
    rabbitmq : RabbitMQConfig = RabbitMQConfig()

    class Config:
        """
        Configuration class for managing environment variables.

        Attributes:
            env_file (str): The name of the environment file.
            env_nested_delimiter (str): The delimiter used for nested environment variables.
        """

        env_file = ".env"
        env_nested_delimiter = "__"


@lru_cache()
def get_config() -> Config:
    log.info("Loading config settings from the environment...")
    return Config()


config = get_config()