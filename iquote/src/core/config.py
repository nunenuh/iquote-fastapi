import logging
import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    AnyHttpUrl,
    ConfigDict,
    EmailStr,
    PostgresDsn,
    field_validator,
)
from pydantic_settings import BaseSettings
from starlette.config import Config

config_env = Config(".env")

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    ENVIRONMENT: str = config_env("ENVIRONMENT", default="development")
    TESTING: bool = config_env("TESTING", default=False)

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    VERSION: str = config_env("VERSION", default="0.1.0")

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = config_env("DOMAIN", default="localhost")
    SERVER_HOST: AnyHttpUrl = config_env("SERVER_HOST", default="localhost")
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'

    # data = config_env("BACKEND_CORS_ORIGINS")
    # data = [i.strip() for i in data.split(",")]
    # for d in data:
    #     print(d)

    BACKEND_CORS_ORIGINS: str = config_env("BACKEND_CORS_ORIGINS")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = config_env("PROJECT_NAME")

    # SENTRY_DSN: Optional[HttpUrl] = None

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return v

    POSTGRES_HOST: str = config_env("POSTGRES_HOST")
    POSTGRES_PORT: str = config_env("POSTGRES_PORT", default="5432")
    POSTGRES_USER: str = config_env("POSTGRES_USER")
    POSTGRES_PASS: str = config_env("POSTGRES_PASS")
    POSTGRES_DB: str = config_env("POSTGRES_DB")
    CONN_STR: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = PostgresDsn(CONN_STR)
    print(SQLALCHEMY_DATABASE_URI)

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn(values.data.get("CONN_STR"))

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @field_validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values.data.get("PROJECT_NAME")
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    # TODO[pydantic]: We couldn't refactor the `validator`, please replace it by `field_validator` manually.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-validators for more information.
    @field_validator("EMAILS_ENABLED")
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.data.get("SMTP_HOST")
            and values.data.get("SMTP_PORT")
            and values.data.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = config_env("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = config_env("FIRST_SUPERUSER_PASSWORD")
    USERS_OPEN_REGISTRATION: bool = False
    model_config = ConfigDict(case_sensitive=True)


settings = Settings()


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return settings


# print(settings.SQLALCHEMY_DATABASE_URI)
