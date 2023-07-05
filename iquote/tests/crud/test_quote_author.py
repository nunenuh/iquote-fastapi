import crud
from faker import Faker
from fastapi.encoders import jsonable_encoder
from schemas.quote_author import QuoteAuthorCreate
from sqlalchemy.orm import Session

# from tests.utils.utils import random_email, random_lower_string

_fake = Faker()


def test_create_quote_author(db: Session) -> None:
    name = _fake.name()
    quote_author_in = QuoteAuthorCreate(
        name=name,
    )
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)
    assert quote_author.name == name


def test_get_quote_author(db: Session) -> None:
    name = _fake.name()
    quote_author_in = QuoteAuthorCreate(name=name)
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)
    quote_author_2 = crud.quote_author.get(db, id=quote_author.id)
    assert quote_author_2
    assert quote_author.name == quote_author_2.name
    assert jsonable_encoder(quote_author) == jsonable_encoder(quote_author_2)


def test_update_quote_author(db: Session) -> None:
    name = _fake.name()
    quote_author_in = QuoteAuthorCreate(name=name)
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)
    quote_author_2 = crud.quote_author.get(db, id=quote_author.id)
    assert quote_author_2
    assert quote_author.name == quote_author_2.name
    assert jsonable_encoder(quote_author) == jsonable_encoder(quote_author_2)


def test_delete_quote_author(db: Session) -> None:
    name = _fake.name()
    quote_author_in = QuoteAuthorCreate(name=name)
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)
    quote_author_2 = crud.quote_author.remove(db, id=quote_author.id)
    quote_author_3 = crud.quote_author.get(db, id=quote_author.id)
    assert quote_author_3 is None
    assert quote_author_2.id == quote_author.id
    assert quote_author_2.name == name
    assert jsonable_encoder(quote_author) == jsonable_encoder(quote_author_2)
