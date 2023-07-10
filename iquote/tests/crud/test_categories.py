from faker import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
from schemas.categories import CategoriesCreate

# from tests.utils.utils import random_email, random_lower_string

_fake = Faker()


def test_create_categories(db: Session) -> None:
    name = _fake.name()
    categories_in = CategoriesCreate(
        name=name,
    )
    categories = crud.categories.create(db, obj_in=categories_in)
    assert categories.name == name


def test_get_categories(db: Session) -> None:
    name = _fake.name()
    categories_in = CategoriesCreate(name=name)
    categories = crud.categories.create(db, obj_in=categories_in)
    categories_2 = crud.categories.get(db, id=categories.id)
    assert categories_2
    assert categories.name == categories_2.name
    assert jsonable_encoder(categories) == jsonable_encoder(categories_2)


def test_get_categories_by_name(db: Session) -> None:
    name = _fake.name()
    categories_in = CategoriesCreate(name=name)
    categories = crud.categories.create(db, obj_in=categories_in)
    categories_2 = crud.categories.get_by_name(db, name=categories.name)
    assert categories_2
    assert categories.name == categories_2.name
    assert jsonable_encoder(categories) == jsonable_encoder(categories_2)


def test_update_categories(db: Session) -> None:
    name = _fake.name()
    categories_in = CategoriesCreate(name=name)
    categories = crud.categories.create(db, obj_in=categories_in)
    categories_2 = crud.categories.get(db, id=categories.id)
    assert categories_2
    assert categories.name == categories_2.name
    assert jsonable_encoder(categories) == jsonable_encoder(categories_2)


def test_delete_categories(db: Session) -> None:
    name = _fake.name()
    categories_in = CategoriesCreate(name=name)
    categories = crud.categories.create(db, obj_in=categories_in)
    categories_2 = crud.categories.remove(db, id=categories.id)
    categories_3 = crud.categories.get(db, id=categories.id)
    assert categories_3 is None
    assert categories_2.id == categories.id
    assert categories_2.name == name
    assert jsonable_encoder(categories) == jsonable_encoder(categories_2)
