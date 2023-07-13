from typing import Optional

from faker import Faker
from sqlalchemy.orm import Session

import crud
import models
from schemas.author import AuthorCreate, AuthorUpdate

_faker = Faker()


def create_random_author(db: Session, *, name: Optional[str] = None) -> models.Author:
    """
    Create a random author in the database.

    Args:
        db (Session): The database session.
        name (str, optional): The name of the author. If not provided, a random name will be generated.

    Returns:
        models.Author: The created author object.
    """
    if not name:
        name = _faker.name()
    author_in = AuthorCreate(name=name, id=id)
    author = crud.author.create(db=db, obj_in=author_in)
    return author


def update_random_author(
    db: Session,
    *,
    retrieved_author: models.Author,
    name: Optional[str] = None,
) -> models.Author:
    """
    Update the name of a random author in the database.

    Args:
        db (Session): The database session.
        retrieved_author (models.Author): The retrieved author object.
        name (Optional[str], optional): The new name for the author. Defaults to None.

    Returns:
        models.Author: The updated author object.
    """
    if not name:
        name = _faker.name()
    author_update_in = AuthorUpdate(name=name)
    updated_author = crud.author.update(
        db, db_obj=retrieved_author, obj_in=author_update_in
    )
    return updated_author
