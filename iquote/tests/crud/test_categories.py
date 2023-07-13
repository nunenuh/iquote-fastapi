from faker import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
from schemas.category import CategoryCreate
from tests.utils.category import (
    create_random_category,
    create_random_category_with_parent,
    update_category_parent_id,
    update_random_category_name,
)

_faker = Faker()


def test_create_category(db: Session) -> None:
    name = _faker.name()
    created_category = create_random_category(db, name=name)
    assert created_category.name == name


def test_create_category_with_parent(db: Session) -> None:
    parent, child1, child2 = create_random_category_with_parent(db)
    assert parent
    assert child1
    assert child2
    assert parent.id == child1.parent_id
    assert parent.id == child2.parent_id
    assert child1.parent_id == child2.parent_id


def test_get_category_by_id(db: Session) -> None:
    name = _faker.name()
    created_category = create_random_category(db, name=name)
    retrieved_category = crud.category.get(db, id=created_category.id)
    assert retrieved_category
    assert retrieved_category.name == created_category.name
    assert jsonable_encoder(created_category) == jsonable_encoder(retrieved_category)


def test_get_category_by_name(db: Session) -> None:
    name = _faker.name()
    created_category = create_random_category(db, name=name)
    retrieved_category = crud.category.get_by_name(db, name=created_category.name)
    assert created_category.name == retrieved_category.name
    assert jsonable_encoder(created_category) == jsonable_encoder(retrieved_category)


def test_get_category_by_parent_id(db: Session) -> None:
    parent, child1, child2 = create_random_category_with_parent(db)
    retrieved_categories = crud.category.get_by_parent_id(db, parent_id=parent.id)
    assert retrieved_categories
    assert len(retrieved_categories) == 2
    assert retrieved_categories[0].id == child1.id
    assert retrieved_categories[1].id == child2.id


def test_update_category(db: Session) -> None:
    name = _faker.name()
    created_category = create_random_category(db, name=name)
    retrieved_category = crud.category.get(db, id=created_category.id)
    update_name = _faker.name()
    updated_category = update_random_category_name(
        db, retrieved_category=retrieved_category, name=update_name
    )
    assert updated_category
    assert created_category.name == retrieved_category.name
    assert updated_category.name == update_name
    assert updated_category.name != name


def test_update_category_parent(db: Session) -> None:
    parent, child1, child2 = create_random_category_with_parent(db)
    old_child1_parent_id = child1.parent_id
    old_child2_parent_id = child2.parent_id

    name = _faker.name()
    new_parent = create_random_category(db, name=name)

    updated_child1 = update_category_parent_id(
        db, retrieved_category=child1, parent_id=new_parent.id
    )

    updated_child2 = update_category_parent_id(
        db, retrieved_category=child2, parent_id=new_parent.id
    )

    assert parent
    assert child1
    assert child2
    assert parent.id == old_child1_parent_id
    assert parent.id == old_child2_parent_id
    assert child1.parent_id == child2.parent_id
    assert updated_child1.parent_id == new_parent.id
    assert updated_child2.parent_id == new_parent.id


def test_delete_category(db: Session) -> None:
    name = _faker.name()
    category_in = CategoryCreate(name=name)
    category = crud.category.create(db, obj_in=category_in)
    category_2 = crud.category.remove(db, id=category.id)
    category_3 = crud.category.get(db, id=category.id)
    assert category_3 is None
    assert category_2.id == category.id
    assert category_2.name == name
    assert jsonable_encoder(category) == jsonable_encoder(category_2)
