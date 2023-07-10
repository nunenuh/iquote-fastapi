from typing import List

from faker import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
from schemas.author import Author, AuthorCreate
from schemas.categories import Categories, CategoriesCreate
from schemas.quote import QuoteCreate, QuoteUpdate

# from tests.utils.utils import random_email, random_lower_string

_fake = Faker()


def test_create_quote(db: Session) -> None:
    text = _fake.sentence()
    quote_in = QuoteCreate(text=text)
    quote = crud.quote.create(db, obj_in=quote_in)
    assert quote.text == text


def test_create_quote_with_author(db: Session) -> None:
    text = _fake.sentence()
    author_name = _fake.name()
    tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    author_in = Author(name=author_name)
    author_in = crud.author.create(db, obj_in=author_in)

    quote_in = QuoteCreate(text=text, tags=tags, author_is=author_in.id)
    quote = crud.quote.create(db, obj_in=quote_in)
    assert quote.text == text
    assert quote


def test_create_quote_with_categories(db: Session) -> None:
    text = _fake.sentence()
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"

    # Create new categories
    category_name_1 = _fake.word()
    category_name_2 = _fake.word()

    category_1 = crud.categories.create(
        db, obj_in=CategoriesCreate(name=category_name_1)
    )
    category_2 = crud.categories.create(
        db, obj_in=CategoriesCreate(name=category_name_2)
    )

    assert category_1.name == category_name_1
    assert category_2.name == category_name_2

    # Create a new quote with the newly created categories
    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        categories=[category_1.id, category_2.id],
    )

    quote = crud.quote.create(db, obj_in=quote_in)

    assert quote.text == text
    assert quote.tags == tags

    # Fetch the quote again from the database to make sure categories were correctly assigned
    quote_db = crud.quote.get(db, id=quote.id)
    category_ids = [category.id for category in quote_db.categories]
    assert category_1.id in category_ids
    assert category_2.id in category_ids


def test_create_quote_with_author_and_categories(db: Session) -> None:
    text = _fake.sentence()
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    author_name = _fake.name()
    category_name_1 = _fake.word()
    category_name_2 = _fake.word()

    author = crud.author.create(db, obj_in=AuthorCreate(name=author_name))
    assert author.name == author_name

    category_1 = crud.categories.create(
        db, obj_in=CategoriesCreate(name=category_name_1)
    )
    assert category_1.name == category_name_1

    category_2 = crud.categories.create(
        db, obj_in=CategoriesCreate(name=category_name_2)
    )
    assert category_2.name == category_name_2

    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        author_id=author.id,
        categories=[category_1.id, category_2.id],
    )

    quote = crud.quote.create(db, obj_in=quote_in)
    assert quote.text == text
    assert quote.tags == tags
    assert quote.author_id == author.id

    quote_db = crud.quote.get(db, id=quote.id)
    assert quote_db
    assert quote_db.author_id == author.id
    category_ids = [category.id for category in quote_db.categories]
    assert category_1.id in category_ids
    assert category_2.id in category_ids


def test_get_quote(db: Session) -> None:
    text = _fake.sentence()
    quote_in = QuoteCreate(text=text)
    quote = crud.quote.create(db, obj_in=quote_in)
    quote_2 = crud.quote.get(db, id=quote.id)
    assert quote_2
    assert quote.text == quote_2.text
    assert jsonable_encoder(quote) == jsonable_encoder(quote_2)


def test_get_quote_with_author_and_categories(db: Session):
    text = _fake.sentence()
    author_name = _fake.name()
    author_in = AuthorCreate(name=author_name)
    author = crud.author.create(db, obj_in=author_in)
    assert author
    assert author.name == author_name

    category_name = _fake.name()
    categories_in = CategoriesCreate(name=category_name)
    categories = crud.categories.create(db, obj_in=categories_in)
    assert categories
    assert categories.name == category_name

    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        author_id=author.id,
        categories_id=categories.id,
    )
    quote = crud.quote.create(db, obj_in=quote_in)
    quote_2 = crud.quote.get(db, id=quote.id)
    assert quote_2
    assert quote.text == quote_2.text
    assert jsonable_encoder(quote) == jsonable_encoder(quote_2)


def test_get_quote_by_author_name(db: Session):
    text = _fake.sentence()
    author_name = _fake.name()
    author_in = AuthorCreate(name=author_name)
    author = crud.author.create(db, obj_in=author_in)
    assert author
    assert author.name == author_name

    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    quote_in = QuoteCreate(text=text, tags=tags, author_id=author.id)
    quote = crud.quote.create(db, obj_in=quote_in)
    quote_2 = crud.quote.get_by_author_id(db, author_id=author.id)
    assert quote_2
    assert quote.text == quote_2.text
    assert jsonable_encoder(quote) == jsonable_encoder(quote_2)


def test_get_quote_by_categories_id(db: Session):
    category_name = _fake.name()
    categories_in = CategoriesCreate(name=category_name)
    categories = crud.categories.create(db, obj_in=categories_in)
    assert categories.name == category_name

    quote_text = _fake.sentence()
    tags = ",".join(_fake.word() for _ in range(3))
    quote_in = QuoteCreate(text=quote_text, tags=tags, categories=[categories.id])
    quote = crud.quote.create(db, obj_in=quote_in)
    quote_2 = crud.quote.get_by_categories_id(db, categories_id=categories.id)
    assert quote.text == quote_2.text
    assert jsonable_encoder(quote) == jsonable_encoder(quote_2)


def test_update_quote(db: Session):
    author_name = _fake.name()
    author_in = AuthorCreate(name=author_name)
    author = crud.author.create(db, obj_in=author_in)

    category_name = _fake.name()
    categories_in = CategoriesCreate(name=category_name)
    categories = crud.categories.create(db, obj_in=categories_in)

    text = _fake.sentence()
    tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        author_id=author.id,
        categories_id=categories.id,
    )
    quote_created = crud.quote.create(db, obj_in=quote_in)

    quote_retrieved = crud.quote.get(db, id=quote_created.id)

    new_text = _fake.sentence()
    new_tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    quote_update_in = QuoteUpdate(
        text=new_text,
        tags=new_tags,
        author_id=author.id,
        categories_id=categories.id,
    )
    quote_updated = crud.quote.update(
        db, db_obj=quote_retrieved, obj_in=quote_update_in
    )

    assert quote_updated.text != text
    assert quote_updated.tags != tags


def test_update_author_and_categories(db: Session):
    author_id = 1
    category_id = 1

    author = crud.author.get(db, id=author_id)
    categories = crud.categories.get(db, id=category_id)

    quote_in = create_quote(author.id, [categories.id])

    quote_created = crud.quote.create(db, obj_in=quote_in)
    quote_retrieved = crud.quote.get(db, id=quote_created.id)

    new_author_id = 2
    new_category_id = 2

    new_author = crud.author.get(db, id=new_author_id)
    new_categories = crud.categories.get(db, id=new_category_id)

    quote_update_in = create_quote_update(new_author.id, [new_categories.id])

    quote_updated = crud.quote.update(
        db, db_obj=quote_retrieved, obj_in=quote_update_in
    )

    assert quote_updated.text == quote_update_in.text
    assert quote_updated.tags == quote_update_in.tags
    assert quote_updated.authors.id == new_author_id
    assert quote_updated.categories[0].id == new_category_id


def create_quote(author_id: int, cat: List[Categories]) -> QuoteCreate:
    text = _fake.sentence()
    tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    return QuoteCreate(text=text, tags=tags, author_id=author_id, categories=cat)


def create_quote_update(author_id: int, cat: List[Categories]) -> QuoteUpdate:
    new_text = _fake.sentence()
    new_tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    return QuoteUpdate(
        text=new_text,
        tags=new_tags,
        author_id=author_id,
        categories=cat,
    )


def test_delete_quote(db: Session):
    quote_in = QuoteCreate(
        text=_fake.sentence(), tags="word", categories_id=1, author_id=1
    )
    quote = crud.quote.create(db, obj_in=quote_in)
    deleted_quote = crud.quote.remove(db, id=quote.id)
    retrieved_quote = crud.quote.get(db, id=quote.id)
    assert retrieved_quote is None
    assert deleted_quote.id == quote.id
    assert deleted_quote.text == quote.text
    assert jsonable_encoder(quote) == jsonable_encoder(deleted_quote)
