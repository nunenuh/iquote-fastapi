from typing import Optional

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.quote import Author, Categories, Quote
from schemas.quote import QuoteCreate, QuoteUpdate
from schemas.user import User


class CRUDQuote(CRUDBase[Quote, QuoteCreate, QuoteUpdate]):
    def get_by_author_id(self, db: Session, *, author_id: int) -> Optional[Quote]:
        return db.query(Quote).filter(Quote.author_id == author_id).first()

    def get_by_author_name(self, db: Session, *, author_name: str) -> Optional[Quote]:
        return (
            db.query(Quote)
            .join(Author)
            .filter(Author.name.ilike(f"%{author_name}%"))
            .all()
        )

    def get_by_categories_id(
        self, db: Session, *, categories_id: int
    ) -> Optional[Quote]:
        return (
            db.query(Quote)
            .join(Quote.categories)
            .filter(Categories.id == categories_id)
            .first()
        )

    def get_by_categories_name(
        self, db: Session, *, categories_name: str
    ) -> Optional[Quote]:
        return (
            db.query(Quote)
            .join(Quote.categories)
            .filter(Categories.name.ilike(f"%{categories_name}%"))
            .all()
        )

    def create(self, db: Session, *, obj_in: QuoteCreate) -> Quote:
        # retrieve or create categories first
        category_objs = []
        for category_id in obj_in.categories:
            category = db.query(Categories).filter(Categories.id == category_id).first()
            if category:
                category_objs.append(category)

        # create quote with categories
        quote_obj = Quote(
            text=obj_in.text,
            tags=obj_in.tags,
            author_id=obj_in.author_id,
            categories=category_objs,
        )
        db.add(quote_obj)
        db.commit()
        db.refresh(quote_obj)
        return quote_obj

    def create_with_new_categories(self, db: Session, *, obj_in: QuoteCreate) -> Quote:
        # retrieve or create categories first
        category_objs = []
        for category_in in obj_in.categories:
            category = (
                db.query(Categories).filter(Categories.id == category_in.id).first()
            )
            if not category:
                category = Categories(name=category_in.name)
                db.add(category)
                db.commit()
                db.refresh(category)
            category_objs.append(category)

        # create quote with categories

        quote_obj = Quote(
            text=obj_in.text,
            tags=obj_in.tags,
            author_id=obj_in.author_id,
            categories=category_objs,
        )
        db.add(quote_obj)
        db.commit()
        db.refresh(quote_obj)
        return quote_obj

    def update(self, db: Session, *, db_obj: Quote, obj_in: QuoteUpdate) -> Quote:
        # Update attributes
        db_obj.text = obj_in.text
        db_obj.tags = obj_in.tags
        db_obj.author_id = obj_in.author_id

        # Clear the existing categories
        db_obj.categories.clear()

        # Update categories
        category_objs = []
        for categories_id in obj_in.categories:
            category = (
                db.query(Categories).filter(Categories.id == categories_id).first()
            )
            if category:
                category_objs.append(category)

        # Add the new categories
        db_obj.categories.extend(category_objs)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def like(self, db: Session, *, user: User, quote: Quote) -> Quote:
        if user in quote.users_who_liked:
            return quote
        quote.users_who_liked.append(user)
        db.add(quote)
        db.commit()
        db.refresh(quote)
        return quote

    def unlike(self, db: Session, *, user: User, quote: Quote) -> Quote:
        if user not in quote.users_who_liked:
            return quote
        quote.users_who_liked.remove(user)
        db.add(quote)
        db.commit()
        db.refresh(quote)
        return quote


quote = CRUDQuote(Quote)
