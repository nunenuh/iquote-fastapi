from typing import Optional

import crud
import models
from schemas.item import ItemCreate
from sqlalchemy.orm import Session
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def create_random_item(db: Session, *, owner_id: Optional[int] = None) -> models.Item:
    if owner_id is None:
        user = create_random_user(db)
        owner_id = user.id
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description, id=id)
    return crud.item.create_with_owner(db=db, obj_in=item_in, owner_id=owner_id)
