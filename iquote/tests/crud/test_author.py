from faker import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
from tests.utils.author import create_random_author, update_random_author

# from tests.utils.utils import random_email, random_lower_string

_faker = Faker()


def test_create_author(db: Session) -> None:
    name = _faker.name()
    author = create_random_author(db, name=name)
    assert author.name == name


def test_get_author(db: Session) -> None:
    name = _faker.name()
    created_author = create_random_author(db, name=name)
    retrieved_author = crud.author.get(db, id=created_author.id)
    assert retrieved_author
    assert created_author.name == retrieved_author.name
    assert jsonable_encoder(created_author) == jsonable_encoder(retrieved_author)


def test_get_author_by_name(db: Session) -> None:
    name = _faker.name()
    created_author = create_random_author(db, name=name)
    retrieved_author = crud.author.get_by_name(db, name=created_author.name)
    assert retrieved_author
    assert created_author.name == retrieved_author.name
    assert jsonable_encoder(created_author) == jsonable_encoder(retrieved_author)


def test_update_author(db: Session) -> None:
    name = _faker.name()
    created_author = create_random_author(db, name=name)
    retrieved_author = crud.author.get(db, id=created_author.id)
    update_name = _faker.name()
    updated_author = update_random_author(
        db, retrieved_author=retrieved_author, name=update_name
    )
    assert updated_author
    assert created_author.name == retrieved_author.name
    assert updated_author.name == update_name
    assert updated_author.name != name


def test_delete_author(db: Session) -> None:
    name = _faker.name()
    created_author = create_random_author(db, name=name)
    removed_author = crud.author.remove(db, id=created_author.id)
    retrieved_author = crud.author.get(db, id=created_author.id)
    assert retrieved_author is None
    assert removed_author.id == created_author.id
    assert removed_author.name == name
    assert jsonable_encoder(created_author) == jsonable_encoder(removed_author)
