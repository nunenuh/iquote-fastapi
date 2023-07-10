from faker import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
from schemas.author import AuthorCreate

# from tests.utils.utils import random_email, random_lower_string

_fake = Faker()


def test_create_author(db: Session) -> None:
    name = _fake.name()
    author_in = AuthorCreate(
        name=name,
    )
    author = crud.author.create(db, obj_in=author_in)
    assert author.name == name


def test_get_author(db: Session) -> None:
    name = _fake.name()
    author_in = AuthorCreate(name=name)
    author = crud.author.create(db, obj_in=author_in)
    author_2 = crud.author.get(db, id=author.id)
    assert author_2
    assert author.name == author_2.name
    assert jsonable_encoder(author) == jsonable_encoder(author_2)


def test_get_author_by_name(db: Session) -> None:
    name = _fake.name()
    author_in = AuthorCreate(name=name)
    author = crud.author.create(db, obj_in=author_in)
    author_2 = crud.author.get_by_name(db, name=author.name)
    assert author_2
    assert author.name == author_2.name
    assert jsonable_encoder(author) == jsonable_encoder(author_2)


def test_update_author(db: Session) -> None:
    name = _fake.name()
    author_in = AuthorCreate(name=name)
    author = crud.author.create(db, obj_in=author_in)
    author_2 = crud.author.get(db, id=author.id)
    assert author_2
    assert author.name == author_2.name
    assert jsonable_encoder(author) == jsonable_encoder(author_2)


def test_delete_author(db: Session) -> None:
    name = _fake.name()
    author_in = AuthorCreate(name=name)
    author = crud.author.create(db, obj_in=author_in)
    author_2 = crud.author.remove(db, id=author.id)
    author_3 = crud.author.get(db, id=author.id)
    assert author_3 is None
    assert author_2.id == author.id
    assert author_2.name == name
    assert jsonable_encoder(author) == jsonable_encoder(author_2)
