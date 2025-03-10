from dataclasses import dataclass
from environs import Env


@dataclass
class PostgresConfig:
    username: str
    password: str
    host: str


@dataclass
class Config:
    db: PostgresConfig


def load_config(path: str = '.env') -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        PostgresConfig(
            username=env.str('POSTGRES_USER'),
            password=env.str('POSTGRES_PASSWORD'),
            host=env.str('DB_HOST'),
        )
    )