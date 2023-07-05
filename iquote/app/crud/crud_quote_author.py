from typing import Any, Dict, Union

from crud.base import CRUDBase
from models.quote import QuoteAuthor
from schemas.quote_author import QuoteAuthorCreate, QuoteAuthorUpdate
from sqlalchemy.orm import Session


class CRUDQuoteAuthor(CRUDBase[QuoteAuthor, QuoteAuthorCreate, QuoteAuthorUpdate]):
    def create(self, db: Session, *, obj_in: QuoteAuthorCreate) -> QuoteAuthor:
        db_obj = QuoteAuthor(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: QuoteAuthor,
        obj_in: Union[QuoteAuthorUpdate, Dict[str, Any]]
    ) -> QuoteAuthor:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


quote_author = CRUDQuoteAuthor(QuoteAuthor)
