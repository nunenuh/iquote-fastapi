from typing import Optional

from faker import Faker
from sqlalchemy.orm import Session

import crud
import models
from schemas.author import AuthorCreate

_faker = Faker()


def create_random_author(
    db: Session, *, owner_id: Optional[int] = None
) -> models.Author:
    name = _faker.name()
    author_in = AuthorCreate(title=name, id=id)
    return crud.author.create(db=db, obj_in=author_in)
