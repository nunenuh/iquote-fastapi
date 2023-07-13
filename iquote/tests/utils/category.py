from typing import List, Optional

from faker import Faker
from sqlalchemy.orm import Session

import crud
import models
from schemas.category import CategoryCreate, CategoryUpdate

_faker = Faker()


def create_random_category(
    db: Session, *, name: Optional[str] = None, parent_id: Optional[int] = None
) -> models.Category:
    """
    Create a random category.

    Args:
        db (Session): The database session.
        name (Optional[str], optional): The name of the category. Defaults to None.
        parent_id (Optional[int], optional): The parent category ID. Defaults to None.

    Returns:
        models.Category: The created category object.
    """

    if name is None:
        name = _faker.name()
    category_in = CategoryCreate(name=name, id=id)
    if parent_id is not None:
        category_in = CategoryCreate(name=name, parent_id=parent_id)
    else:
        category_in = CategoryCreate(name=name)

    category = crud.category.create(db=db, obj_in=category_in)
    return category


def create_random_category_with_parent(
    db: Session, *, parent_id: Optional[int] = None
) -> List[models.Category]:
    """
    Create a random category with an optional parent category.

    Parameters:
        db (Session): The database session.
        parent_id (Optional[int], optional): The ID of the parent category. Defaults to None.

    Returns:
        List[models.Category]: A list containing the newly created parent category and its two child categories.
    """
    if parent_id is None:
        category_parent = create_random_category(db)
    else:
        category_parent = create_random_category(db, parent_id=parent_id)

    category_child1 = create_random_category(db, parent_id=category_parent.id)
    category_child2 = create_random_category(db, parent_id=category_parent.id)

    return [category_parent, category_child1, category_child2]


def update_random_category_name(
    db: Session,
    *,
    retrieved_category: models.Category,
    name: Optional[str] = None,
) -> models.Category:
    if not name:
        name = _faker.name()
    category_update_in = CategoryUpdate(name=name)
    updated_category = crud.category.update(
        db, db_obj=retrieved_category, obj_in=category_update_in
    )
    return updated_category


def update_category_parent_id(
    db: Session,
    *,
    retrieved_category: models.Category,
    parent_id: Optional[int],
) -> models.Category:
    category_update_in = CategoryUpdate(
        name=retrieved_category.name, parent_id=parent_id
    )
    updated_category = crud.category.update(
        db, db_obj=retrieved_category, obj_in=category_update_in
    )
    return updated_category
