import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True, frozen=True, kw_only=True)
class MaxConfig:
    token: str


@dataclass(slots=True, frozen=True, kw_only=True)
class DbConfig:
    protocol: str = "postgresql+psycopg"
    host: str
    port: int
    user: str
    password: str
    db_name: str

    @property
    def uri(self) -> str:
        return f"{self.protocol}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass(slots=True, frozen=True, kw_only=True)
class RedisConfig:
    host: str
    port: int
    password: str | None = None
    database: int = 0

    @property
    def uri(self) -> str:
        password = "" if self.password is None else f":{self.password}@"
        return f"redis://{password}{self.host}:{self.port}/{self.database}"


@dataclass(slots=True, frozen=True, kw_only=True)
class SchedulerConfig:
    tasks_key: str = "maxhack"


@dataclass(slots=True, frozen=True, kw_only=True)
class AppConfig:
    host: str = "localhost"
    port: int = 7001
    cors_policy_disabled: bool = True
    cors: list[str] = field(default_factory=list[str])
    additional_debug: bool = False


@dataclass(slots=True, frozen=True, kw_only=True)
class SwaggerConfig:
    root_path: str = ""


@dataclass(slots=True, frozen=True, kw_only=True)
class Config:
    max: MaxConfig
    db: DbConfig
    redis: RedisConfig
    scheduler: SchedulerConfig
    app: AppConfig
    swagger: SwaggerConfig
    log_level: str


def load_config(env: str | Path | None = None) -> Config:
    if env:
        from dotenv import load_dotenv

        load_dotenv(env)

    return Config(
        max=MaxConfig(token=os.environ["MAX_TOKEN"]),
        db=DbConfig(
            host=os.environ["DB_HOST"],
            port=int(os.environ["DB_PORT"]),
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            db_name=os.environ["DB_NAME"],
            protocol=os.getenv("DB_PROTOCOL", "postgresql+psycopg"),
        ),
        redis=RedisConfig(
            host=os.environ["REDIS_HOST"],
            port=int(os.environ["REDIS_PORT"]),
            password=os.getenv("REDIS_PASSWORD", None),
            database=int(os.getenv("REDIS_DB", 0)),
        ),
        scheduler=SchedulerConfig(),
        app=AppConfig(
            host=os.getenv("API_HOST", "localhost"),
            port=int(os.getenv("API_PORT", 7001)),
            cors_policy_disabled=(
                os.getenv("CORS_POLICY_DISABLED", "True").lower() == "true"
            ),
            cors=os.getenv("CORS", "").split(","),
            additional_debug=os.getenv("ADDITIONAL_DEBUG", "False").lower() == "true",
        ),
        swagger=SwaggerConfig(
            root_path=os.getenv("ROOT_PATH", ""),
        ),
        log_level=os.getenv("LOG_LEVEL", "DEBUG"),
    )
