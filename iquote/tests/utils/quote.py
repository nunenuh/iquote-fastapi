from typing import Optional, Tuple

from faker import Faker
from sqlalchemy.orm import Session

import crud
import models
from schemas.quote import QuoteCreate, QuoteUpdate
from tests.utils.author import create_random_author
from tests.utils.category import create_random_category

_faker = Faker()


def create_random_quote(
    db: Session,
    *,
    text: Optional[str] = None,
    tags: Optional[str] = None,
) -> models.Quote:
    if text is None:
        text = _faker.sentence()

    if tags is None:
        tags = f"{_faker.word()},{_faker.word()},{_faker.word()}"

    quote_in = QuoteCreate(text=text, tags=tags, id=id)
    quote = crud.quote.create(db=db, obj_in=quote_in)
    return quote


def create_random_quote_with_random_author(
    db: Session,
    *,
    text: Optional[str] = None,
    tags: Optional[str] = None,
    author: Optional[models.Author] = None,
) -> Tuple[models.Quote, models.Author]:
    if text is None:
        text = _faker.sentence()
    if tags is None:
        tags = f"{_faker.word()},{_faker.word()},{_faker.word()}"
    if author is None:
        author = create_random_author(db=db)
    quote_in = QuoteCreate(text=text, tags=tags, author_id=author.id)
    quote = crud.quote.create(db=db, obj_in=quote_in)
    return quote, author


def create_random_quote_with_random_category(
    db: Session,
    *,
    text: Optional[str] = None,
    tags: Optional[str] = None,
) -> Tuple[models.Quote, models.Category, models.Category]:
    if text is None:
        text = _faker.sentence()
    if tags is None:
        tags = f"{_faker.word()},{_faker.word()},{_faker.word()}"

    category1 = create_random_category(db=db)
    category2 = create_random_category(db=db)
    quote_in = QuoteCreate(
        text=text, tags=tags, categories=[category1.id, category2.id]
    )
    quote = crud.quote.create(db=db, obj_in=quote_in)
    return quote, category1, category2


def create_random_quote_with_random_author_and_category(
    db: Session,
    *,
    text: Optional[str] = None,
    tags: Optional[str] = None,
    author: Optional[models.Author] = None,
) -> Tuple[models.Quote, models.Author, models.Category, models.Category]:
    if text is None:
        text = _faker.sentence()
    if tags is None:
        tags = f"{_faker.word()},{_faker.word()},{_faker.word()}"
    if author is None:
        author = create_random_author(db=db)

    category1 = create_random_category(db=db)
    category2 = create_random_category(db=db)
    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        author_id=author.id,
        categories=[category1.id, category2.id],
    )
    quote = crud.quote.create(db=db, obj_in=quote_in)
    return quote, author, category1, category2


def update_random_quote(
    db: Session,
    *,
    retrieved_quote: models.Quote,
    text: Optional[str] = None,
    tags: Optional[str] = None,
) -> models.Quote:
    if text is None:
        text = _faker.sentence()
    if tags is None:
        tags = f"{_faker.word()},{_faker.word()},{_faker.word()}"
    quote_update_in = QuoteUpdate(text=text, tags=tags)
    updated_quote = crud.quote.update(
        db, db_obj=retrieved_quote, obj_in=quote_update_in
    )
    return updated_quote


def update_random_quote_with_random_author(
    db: Session,
    *,
    retrieved_quote: models.Quote,
    retrieved_author: Optional[models.Author] = None,
    text: Optional[str] = None,
    tags: Optional[str] = None,
) -> Tuple[models.Quote, models.Author]:
    if text is None:
        text = _faker.sentence()
    if tags is None:
        tags = f"{_faker.word()},{_faker.word()},{_faker.word()}"

    if retrieved_author is None:
        retrieved_author = create_random_author(db=db)
    quote_update_in = QuoteUpdate(text=text, tags=tags, author_id=retrieved_author.id)
    updated_quote = crud.quote.update(
        db, db_obj=retrieved_quote, obj_in=quote_update_in
    )
    return updated_quote, retrieved_author


def update_random_quote_with_random_categories(
    db: Session,
    *,
    retrieved_quote: models.Quote,
    text: Optional[str] = None,
    tags: Optional[str] = None,
) -> Tuple[models.Quote, models.Category, models.Category]:
    if text is None:
        text = _faker.sentence()
    if tags is None:
        tags = f"{_faker.word()},{_faker.word()},{_faker.word()}"

    category1 = create_random_category(db=db)
    category2 = create_random_category(db=db)
    quote_update_in = QuoteUpdate(
        text=text, tags=tags, categories=[category1.id, category2.id]
    )
    updated_quote = crud.quote.update(
        db, db_obj=retrieved_quote, obj_in=quote_update_in
    )
    return updated_quote, category1, category2


def update_random_quote_with_random_author_and_categories(
    db: Session,
    *,
    retrieved_quote: models.Quote,
    text: Optional[str] = None,
    tags: Optional[str] = None,
) -> Tuple[models.Quote, models.Author, models.Category, models.Category]:
    if text is None:
        text = _faker.sentence()
    if tags is None:
        tags = f"{_faker.word()},{_faker.word()},{_faker.word()}"

    created_author = create_random_author(db=db)
    category1 = create_random_category(db=db)
    category2 = create_random_category(db=db)
    quote_update_in = QuoteUpdate(
        text=text,
        tags=tags,
        author_id=created_author.id,
        categories=[category1.id, category2.id],
    )
    updated_quote = crud.quote.update(
        db, db_obj=retrieved_quote, obj_in=quote_update_in
    )
    return updated_quote, created_author, category1, category2
