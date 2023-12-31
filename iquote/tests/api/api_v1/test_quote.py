from typing import Dict

import faker
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.config import settings

_fake = faker.Faker()


def test_create_quote(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {
        "text": _fake.sentence(),
        "tags": f"{_fake.words()},{_fake.words()},{_fake.words()}",
    }

    response = client.post(
        f"{settings.API_V1_STR}/quote/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == data["text"]
    assert content["tags"] == data["tags"]
    assert "id" in content


def test_update_quote(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    quote_id = 1
    data = {"text": _fake.name()}
    response = client.put(
        f"{settings.API_V1_STR}/quote/{quote_id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == data["text"]
    assert "id" in content
    assert content["id"] == quote_id


def test_get_quote_list(
    client: TestClient, normal_user_token_headers: Dict[str, str], db: Session
) -> None:
    r = client.get(
        f"{settings.API_V1_STR}/quote"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert isinstance(rjson, list)
    assert rjson[0]["text"]
    assert rjson[0]["id"]


def test_get_quote(
    client: TestClient,
) -> None:
    quote_id = 1
    r = client.get(
        f"{settings.API_V1_STR}/quote/{quote_id}"
        # headers=normal_user_token_headers
    )

    assert r.status_code == 200
    rjson = r.json()
    assert rjson
    assert rjson["id"] == quote_id


def test_create_quote_with_categories_and_author(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    author_id = 1
    category_id = 1
    data = {
        "text": _fake.sentence(),
        "tags": f"{_fake.words()},{_fake.words()},{_fake.words()}",
        "author_id": author_id,
        "categories": [category_id],
    }

    response = client.post(
        f"{settings.API_V1_STR}/quote/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == data["text"]
    assert content["tags"] == data["tags"]
    assert "id" in content


def test_update_quote_with_author_categories(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    quote_id = 1
    new_text = _fake.sentence()
    new_tags = ",".join([_fake.word() for _ in range(3)])
    new_author_id = 1
    new_category_id = 1
    data = {
        "text": new_text,
        "tags": new_tags,
        "author_id": new_author_id,
        "categories": [new_category_id],
    }
    response = client.put(
        f"{settings.API_V1_STR}/quote/{quote_id}",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert response.status_code == 200
    assert content["id"] == quote_id
    assert content["text"] == new_text
    assert content["tags"] == new_tags
    assert content["author_id"] == new_author_id
    assert content["categories"][0]["id"] == new_category_id


def test_like_quote_normal_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    quote_id = 1
    response = client.put(
        f"{settings.API_V1_STR}/quote/{quote_id}/like",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["id"] == quote_id
    assert content["liked"] == True


def test_like_quote_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    quote_id = 1
    response = client.put(
        f"{settings.API_V1_STR}/quote/{quote_id}/like",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["id"] == quote_id
    assert content["liked"] == True


def test_unlike_quote_normal_user(
    client: TestClient, normal_user_token_headers: dict, db: Session
) -> None:
    quote_id = 1
    response = client.put(
        f"{settings.API_V1_STR}/quote/{quote_id}/unlike",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["id"] == quote_id
    assert content["liked"] == False


def test_unlike_quote_superuser(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    quote_id = 1
    response = client.put(
        f"{settings.API_V1_STR}/quote/{quote_id}/unlike",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["id"] == quote_id
    assert content["liked"] == False


def test_delete_quote(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    data = {"text": _fake.name()}
    response = client.post(
        f"{settings.API_V1_STR}/quote/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["text"] == data["text"]
    assert "id" in content

    quote_id = content["id"]
    response = client.delete(
        f"{settings.API_V1_STR}/quote/{quote_id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert content["id"] == quote_id
