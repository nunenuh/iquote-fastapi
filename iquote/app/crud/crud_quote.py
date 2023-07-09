from typing import Optional

from crud.base import CRUDBase
from models.quote import Quote, QuoteAuthor, QuoteCategories
from schemas.quote import QuoteCreate, QuoteUpdate
from sqlalchemy.orm import Session


class CRUDQuote(CRUDBase[Quote, QuoteCreate, QuoteUpdate]):
    def get_by_author_id(self, db: Session, *, author_id: int) -> Optional[Quote]:
        return db.query(Quote).filter(Quote.author_id == author_id).first()

    def get_by_author_name(self, db: Session, *, author_name: str) -> Optional[Quote]:
        return (
            db.query(Quote)
            .join(QuoteAuthor)
            .filter(QuoteAuthor.name.ilike(f"%{author_name}%"))
            .all()
        )

    def get_by_categories_id(
        self, db: Session, *, categories_id: int
    ) -> Optional[Quote]:
        return db.query(Quote).filter(Quote.categories_id == categories_id).first()

    def get_by_categories_name(
        self, db: Session, *, categories_name: str
    ) -> Optional[Quote]:
        return (
            db.query(Quote)
            .join(QuoteCategories)
            .filter(QuoteCategories.name.ilike(f"%{categories_name}%"))
            .all()
        )

    # def create(self, db: Session, *, obj_in: QuoteCreate) -> Quote:
    #     db_obj = Quote(text=obj_in.text)
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def update(
    #     self,
    #     db: Session,
    #     *,
    #     db_obj: Quote,
    #     obj_in: Union[QuoteUpdate, Dict[str, Any]]
    # ) -> Quote:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)

    #     return super().update(db, db_obj=db_obj, obj_in=update_data)


quote = CRUDQuote(Quote)
