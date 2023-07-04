from typing import Dict, Generator

import pytest
from app.core.config import settings
from app.db.session import SessionLocal
from app.main import create_application  # updated
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette.testclient import TestClient
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


# @pytest.fixture(scope="module")
# def test_app():
#     # set up
#     app = create_application()
#     app.dependency_overrides[get_settings] = get_settings_override
#     with TestClient(app) as test_client:
#         # testing
#         yield test_client


# @pytest.fixture(scope="module")
# def test_app_with_db():
#     app = create_application()
#     app.dependency_overrides[get_settings] = get_settings_override
#     register_tortoise(
#         app,
#         db_url=os.environ.get("DATABASE_TEST_URL"),
#         modules={"models": ["app.models.tortoise"]},
#         generate_schemas=True,
#         add_exception_handlers=True,
#     )

#     with TestClient(app) as test_client:
#         yield test_client
