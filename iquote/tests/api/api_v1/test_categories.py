from typing import Dict

import faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.config import settings

_fake = faker.Faker()


def test_get_categories_list(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/categories"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert isinstance(rjson, list)
    assert rjson[0]["name"]
    assert rjson[0]["id"]


def test_get_categories(
    client: TestClient,
) -> None:
    categories_id = 1
    r = client.get(
        f"{settings.API_V1_STR}/categories/{categories_id}"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert rjson["id"] == categories_id


def test_get_quote_category_by_name(
    client: TestClient,
) -> None:
    category_name = "James King"
    r = client.get(
        f"{settings.API_V1_STR}/categories/name/{category_name}"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert rjson["name"] == category_name


def test_get_quote_category_by_parent_id(
    client: TestClient,
) -> None:
    parent_id = 15
    r = client.get(
        f"{settings.API_V1_STR}/categories/parent/{parent_id}"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert type(rjson) == list
    assert rjson[0]["parent_id"] == parent_id


def test_create_categories(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": _fake.name()}
    response = client.post(
        f"{settings.API_V1_STR}/categories",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_update_categories(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    categories_id = 1
    data = {"name": _fake.name()}
    response = client.put(
        f"{settings.API_V1_STR}/categories/{categories_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content
    assert content["id"] == categories_id


def test_delete_categories(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": _fake.name()}
    response = client.post(
        f"{settings.API_V1_STR}/categories",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content

    categories_id = content["id"]
    response = client.delete(
        f"{settings.API_V1_STR}/categories/{categories_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["id"] == categories_id
