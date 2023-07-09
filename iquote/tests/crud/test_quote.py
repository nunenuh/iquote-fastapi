import crud
from faker import Faker
from fastapi.encoders import jsonable_encoder
from schemas.quote import QuoteCreate, QuoteUpdate
from schemas.quote_author import QuoteAuthor, QuoteAuthorCreate
from schemas.quote_categories import QuoteCategories, QuoteCategoriesCreate
from sqlalchemy.orm import Session

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
    quote_author_in = QuoteAuthor(name=author_name)
    quote_author_in = crud.quote_author.create(db, obj_in=quote_author_in)

    quote_in = QuoteCreate(text=text, tags=tags, author_is=quote_author_in.id)
    quote = crud.quote.create(db, obj_in=quote_in)
    assert quote.text == text
    assert quote


def test_create_quote_with_categories(db: Session) -> None:
    text = _fake.sentence()
    tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    category_name = _fake.name()
    quote_categories_in = QuoteCategories(name=category_name)
    quote_categories_in = crud.quote_categories.create(db, obj_in=quote_categories_in)

    quote_in = QuoteCreate(text=text, tags=tags, categories_id=quote_categories_in.id)
    quote = crud.quote.create(db, obj_in=quote_in)
    assert quote.text == text
    assert quote


def test_create_quote_with_author_and_categories(db: Session) -> None:
    text = _fake.sentence()
    author_name = _fake.name()
    quote_author_in = QuoteAuthorCreate(name=author_name)
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)
    assert quote_author
    assert quote_author.name == author_name

    category_name = _fake.name()
    quote_categories_in = QuoteCategoriesCreate(name=category_name)
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    assert quote_categories
    assert quote_categories.name == category_name

    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        author_id=quote_author.id,
        categories_id=quote_categories.id,
    )
    quote = crud.quote.create(db, obj_in=quote_in)
    assert quote
    assert quote.text == text
    assert quote.tags == tags
    assert quote.authors.id == quote_author.id
    assert quote.categories.id == quote_categories.id


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
    quote_author_in = QuoteAuthorCreate(name=author_name)
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)
    assert quote_author
    assert quote_author.name == author_name

    category_name = _fake.name()
    quote_categories_in = QuoteCategoriesCreate(name=category_name)
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    assert quote_categories
    assert quote_categories.name == category_name

    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        author_id=quote_author.id,
        categories_id=quote_categories.id,
    )
    quote = crud.quote.create(db, obj_in=quote_in)
    quote_2 = crud.quote.get(db, id=quote.id)
    assert quote_2
    assert quote.text == quote_2.text
    assert jsonable_encoder(quote) == jsonable_encoder(quote_2)


def test_get_quote_by_author_name(db: Session):
    text = _fake.sentence()
    author_name = _fake.name()
    quote_author_in = QuoteAuthorCreate(name=author_name)
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)
    assert quote_author
    assert quote_author.name == author_name

    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    quote_in = QuoteCreate(text=text, tags=tags, author_id=quote_author.id)
    quote = crud.quote.create(db, obj_in=quote_in)
    quote_2 = crud.quote.get_by_author_id(db, author_id=quote_author.id)
    assert quote_2
    assert quote.text == quote_2.text
    assert jsonable_encoder(quote) == jsonable_encoder(quote_2)


def test_get_quote_by_categories_id(db: Session):
    text = _fake.sentence()
    category_name = _fake.name()

    quote_categories_in = QuoteCategoriesCreate(name=category_name)
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    assert quote_categories
    assert quote_categories.name == category_name

    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    quote_in = QuoteCreate(text=text, tags=tags, categories_id=quote_categories.id)
    quote = crud.quote.create(db, obj_in=quote_in)
    quote_2 = crud.quote.get_by_categories_id(db, categories_id=quote_categories.id)
    assert quote_2
    assert quote.text == quote_2.text
    assert jsonable_encoder(quote) == jsonable_encoder(quote_2)


def test_update_quote(db: Session):
    author_name = _fake.name()
    quote_author_in = QuoteAuthorCreate(name=author_name)
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)

    category_name = _fake.name()
    quote_categories_in = QuoteCategoriesCreate(name=category_name)
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)

    text = _fake.sentence()
    tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        author_id=quote_author.id,
        categories_id=quote_categories.id,
    )
    quote_created = crud.quote.create(db, obj_in=quote_in)

    quote_retrieved = crud.quote.get(db, id=quote_created.id)

    new_text = _fake.sentence()
    new_tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    quote_update_in = QuoteUpdate(
        text=new_text,
        tags=new_tags,
        author_id=quote_author.id,
        categories_id=quote_categories.id,
    )
    quote_updated = crud.quote.update(
        db, db_obj=quote_retrieved, obj_in=quote_update_in
    )

    assert quote_updated.text != text
    assert quote_updated.tags != tags


def test_update_quote_author_and_categories(db: Session):
    author_id = 1
    category_id = 1

    quote_author = crud.quote_author.get(db, id=author_id)
    quote_categories = crud.quote_categories.get(db, id=category_id)

    text = _fake.sentence()
    tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    quote_in = QuoteCreate(
        text=text,
        tags=tags,
        author_id=quote_author.id,
        categories_id=quote_categories.id,
    )

    quote_created = crud.quote.create(db, obj_in=quote_in)
    quote_retrieved = crud.quote.get(db, id=quote_created.id)

    new_text = _fake.sentence()
    new_tags = f"{_fake.words()},{_fake.words()},{_fake.words()}"
    new_author_id = 2
    new_category_id = 2

    quote_update_in = QuoteUpdate(
        text=new_text,
        tags=new_tags,
        author_id=new_author_id,
        categories_id=new_category_id,
    )
    quote_updated = crud.quote.update(
        db, db_obj=quote_retrieved, obj_in=quote_update_in
    )

    assert quote_updated.text == new_text
    assert quote_updated.tags == new_tags
    assert quote_updated.authors.id == new_author_id
    assert quote_updated.categories.id == new_category_id


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
