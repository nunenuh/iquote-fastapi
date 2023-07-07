from typing import Any, Dict, List, Optional, Union

from crud.base import CRUDBase
from models.quote import QuoteCategories
from schemas.quote_categories import (
    QuoteCategoriesCreate,
    QuoteCategoriesUpdate,
)
from sqlalchemy.orm import Session


class CRUDQuoteCategories(
    CRUDBase[QuoteCategories, QuoteCategoriesCreate, QuoteCategoriesUpdate]
):
    def get_by_name(self, db: Session, *, name: str) -> Optional[QuoteCategories]:
        return db.query(QuoteCategories).filter(QuoteCategories.name == name).first()

    def get_by_parent_id(self, db: Session, *, parent_id: int) -> List[QuoteCategories]:
        return (
            db.query(QuoteCategories)
            .filter(QuoteCategories.parent_id == parent_id)
            .all()
        )

    def get_by_parent_name(
        self, db: Session, *, parent_name: str
    ) -> List[QuoteCategories]:
        return (
            db.query(QuoteCategories)
            .join(QuoteCategories.parent)
            .filter(QuoteCategories.parent.has(name=parent_name))
            .all()
        )

    def create_by_parent(
        self, db: Session, parent_id: int, obj_in: QuoteCategoriesCreate
    ) -> QuoteCategories:
        db_obj = QuoteCategories(**obj_in.dict(), parent_id=parent_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create(self, db: Session, *, obj_in: QuoteCategoriesCreate) -> QuoteCategories:
        db_obj = QuoteCategories(name=obj_in.name)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: QuoteCategories,
        obj_in: Union[QuoteCategoriesUpdate, Dict[str, Any]]
    ) -> QuoteCategories:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


quote_categories = CRUDQuoteCategories(QuoteCategories)
