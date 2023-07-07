import crud
from faker import Faker
from fastapi.encoders import jsonable_encoder
from schemas.quote_categories import QuoteCategoriesCreate
from sqlalchemy.orm import Session

# from tests.utils.utils import random_email, random_lower_string

_fake = Faker()


def test_create_quote_categories(db: Session) -> None:
    name = _fake.name()
    quote_categories_in = QuoteCategoriesCreate(
        name=name,
    )
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    assert quote_categories.name == name


def test_get_quote_categories(db: Session) -> None:
    name = _fake.name()
    quote_categories_in = QuoteCategoriesCreate(name=name)
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    quote_categories_2 = crud.quote_categories.get(db, id=quote_categories.id)
    assert quote_categories_2
    assert quote_categories.name == quote_categories_2.name
    assert jsonable_encoder(quote_categories) == jsonable_encoder(quote_categories_2)


def test_get_quote_categories_by_name(db: Session) -> None:
    name = _fake.name()
    quote_categories_in = QuoteCategoriesCreate(name=name)
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    quote_categories_2 = crud.quote_categories.get_by_name(
        db, name=quote_categories.name
    )
    assert quote_categories_2
    assert quote_categories.name == quote_categories_2.name
    assert jsonable_encoder(quote_categories) == jsonable_encoder(quote_categories_2)


def test_update_quote_categories(db: Session) -> None:
    name = _fake.name()
    quote_categories_in = QuoteCategoriesCreate(name=name)
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    quote_categories_2 = crud.quote_categories.get(db, id=quote_categories.id)
    assert quote_categories_2
    assert quote_categories.name == quote_categories_2.name
    assert jsonable_encoder(quote_categories) == jsonable_encoder(quote_categories_2)


def test_delete_quote_categories(db: Session) -> None:
    name = _fake.name()
    quote_categories_in = QuoteCategoriesCreate(name=name)
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    quote_categories_2 = crud.quote_categories.remove(db, id=quote_categories.id)
    quote_categories_3 = crud.quote_categories.get(db, id=quote_categories.id)
    assert quote_categories_3 is None
    assert quote_categories_2.id == quote_categories.id
    assert quote_categories_2.name == name
    assert jsonable_encoder(quote_categories) == jsonable_encoder(quote_categories_2)
