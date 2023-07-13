import faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.config import settings

_fake = faker.Faker()


def test_create_category(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": _fake.name()}
    response = client.post(
        f"{settings.API_V1_STR}/category",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content


def test_update_category(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    category_id = 1
    data = {"name": _fake.name()}
    response = client.put(
        f"{settings.API_V1_STR}/category/{category_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content
    assert content["id"] == category_id


def test_get_category_list(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/category"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert isinstance(rjson, list)
    assert rjson[0]["name"]
    assert rjson[0]["id"]


def test_get_category(
    client: TestClient,
) -> None:
    category_id = 1
    r = client.get(
        f"{settings.API_V1_STR}/category/{category_id}"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert rjson["id"] == category_id


def test_get_quote_category_by_name(
    client: TestClient,
) -> None:
    category_id = 1
    r = client.get(
        f"{settings.API_V1_STR}/category/{category_id}"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert rjson["id"] == category_id

    category_name = rjson["name"]
    r = client.get(
        f"{settings.API_V1_STR}/category/name/{category_name}"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert rjson["name"] == category_name


def test_get_quote_category_by_parent_id(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data1 = {"name": _fake.name()}
    response = client.post(
        f"{settings.API_V1_STR}/category",
        headers=superuser_token_headers,
        json=data1,
    )
    assert response.status_code == 200
    content1 = response.json()
    assert content1["name"] == data1["name"]
    assert "id" in content1

    data2 = {"name": _fake.name(), "parent_id": content1["id"]}
    response = client.post(
        f"{settings.API_V1_STR}/category",
        headers=superuser_token_headers,
        json=data2,
    )
    assert response.status_code == 200
    content2 = response.json()
    assert content2["name"] == data2["name"]
    assert "id" in content2

    parent_id = content1["id"]
    r = client.get(
        f"{settings.API_V1_STR}/category/parent/{parent_id}"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert type(rjson) == list
    assert rjson[0]["parent_id"] == parent_id


def test_delete_category(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"name": _fake.name()}
    response = client.post(
        f"{settings.API_V1_STR}/category",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert "id" in content

    category_id = content["id"]
    response = client.delete(
        f"{settings.API_V1_STR}/category/{category_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["id"] == category_id
