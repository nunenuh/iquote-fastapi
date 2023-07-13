from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.author import Author
from schemas.author import AuthorCreate, AuthorUpdate


class CRUDAuthor(CRUDBase[Author, AuthorCreate, AuthorUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Author]:
        return db.query(Author).filter(Author.name == name).first()

    def create(self, db: Session, *, obj_in: AuthorCreate) -> Author:
        db_obj = Author(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Author,
        obj_in: Union[AuthorUpdate, Dict[str, Any]]
    ) -> Author:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


author = CRUDAuthor(Author)
