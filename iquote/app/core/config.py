import logging
import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, PostgresDsn, validator
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

    @validator("BACKEND_CORS_ORIGINS", pre=True)
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
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = PostgresDsn.build(
        scheme="postgresql",
        user=POSTGRES_USER,
        password=POSTGRES_PASS,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        path=f"/{POSTGRES_DB or ''}",
    )
    print(SQLALCHEMY_DATABASE_URI)

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = config_env("FIRST_SUPERUSER")
    FIRST_SUPERUSER_PASSWORD: str = config_env("FIRST_SUPERUSER_PASSWORD")
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return settings


# print(settings.SQLALCHEMY_DATABASE_URI)
