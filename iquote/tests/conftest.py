from typing import Dict, Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from core.config import settings
from db.session import SessionLocal
from main import create_application  # updated
from tests.utils.user import authentication_token_from_email
from tests.utils.utils import get_superuser_token_headers


def get_settings_override():
    settings.TESTING = True
    return settings


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()


@pytest.fixture(scope="module")
def client() -> Generator:
    app = create_application()
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> Dict[str, str]:
    return get_superuser_token_headers(client)


@pytest.fixture(scope="module")
def normal_user_token_headers(client: TestClient, db: Session) -> Dict[str, str]:
    settings = get_settings_override()
    return authentication_token_from_email(
        client=client, email=settings.EMAIL_TEST_USER, db=db
    )
