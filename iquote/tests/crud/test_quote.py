from faker import Faker
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import crud
from schemas.quote import QuoteCreate
from schemas.user import UserCreate
from tests.utils.quote import (
    create_random_quote,
    create_random_quote_with_random_author,
    create_random_quote_with_random_author_and_category,
    create_random_quote_with_random_category,
    update_random_quote,
    update_random_quote_with_random_author,
    update_random_quote_with_random_author_and_categories,
)

# from tests.utils.utils import random_email, random_lower_string

_fake = Faker()


def test_create_quote(db: Session) -> None:
    text = _fake.sentence()
    quote = create_random_quote(db, text=text)
    assert quote.text == text


def test_create_quote_with_author(db: Session) -> None:
    text = _fake.sentence()
    quote, author = create_random_quote_with_random_author(db, text=text)
    assert quote.text == text
    assert quote.authors == author


def test_create_quote_with_categories(db: Session) -> None:
    text = _fake.sentence()
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    quote, cat1, cat2 = create_random_quote_with_random_category(
        db, text=text, tags=tags
    )

    assert quote
    assert cat1
    assert cat2
    assert quote.text == text
    assert quote.tags == tags
    assert cat1 in quote.categories
    assert cat2 in quote.categories


def test_create_quote_with_author_and_categories(db: Session) -> None:
    text = _fake.sentence()
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"

    quote, author, cat1, cat2 = create_random_quote_with_random_author_and_category(
        db, text=text, tags=tags
    )

    assert quote
    assert author
    assert cat1
    assert cat2

    assert quote.authors == author
    assert cat1 in quote.categories
    assert cat2 in quote.categories


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
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"

    quote, author, cat1, cat2 = create_random_quote_with_random_author_and_category(
        db, text=text, tags=tags
    )

    retrieved_quote = crud.quote.get(db, id=quote.id)

    assert quote
    assert retrieved_quote
    assert author
    assert cat1
    assert cat2

    assert retrieved_quote.authors == author
    assert cat1 in retrieved_quote.categories
    assert cat2 in retrieved_quote.categories
    assert quote.text == retrieved_quote.text
    assert jsonable_encoder(quote) == jsonable_encoder(retrieved_quote)


def test_get_quote_by_author_id(db: Session):
    text = _fake.sentence()
    created_quote, created_author = create_random_quote_with_random_author(
        db, text=text
    )
    retrieved_quote = crud.quote.get_by_author_id(db, author_id=created_author.id)
    assert created_quote.text == text
    assert created_quote.authors == created_author
    assert retrieved_quote
    assert created_quote.text == retrieved_quote.text
    assert jsonable_encoder(created_quote) == jsonable_encoder(retrieved_quote)


def test_get_quote_by_categories_id(db: Session):
    text = _fake.sentence()
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    created_quote, cat1, cat2 = create_random_quote_with_random_category(
        db, text=text, tags=tags
    )

    retrieved_quote1 = crud.quote.get_by_categories_id(db, categories_id=cat1.id)
    retrieved_quote2 = crud.quote.get_by_categories_id(db, categories_id=cat2.id)
    assert created_quote.text == retrieved_quote1.text
    assert created_quote.text == retrieved_quote2.text
    assert cat1 in retrieved_quote1.categories
    assert cat2 in retrieved_quote1.categories
    assert cat1 in retrieved_quote2.categories
    assert cat2 in retrieved_quote2.categories
    assert jsonable_encoder(created_quote) == jsonable_encoder(retrieved_quote1)
    assert jsonable_encoder(created_quote) == jsonable_encoder(retrieved_quote2)


def test_update_quote(db: Session):
    text = _fake.sentence()
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    created_quote = create_random_quote(db, text=text, tags=tags)
    retrieved_quote = crud.quote.get(db, id=created_quote.id)
    assert retrieved_quote.text == text
    assert retrieved_quote.tags == tags

    updated_text = _fake.sentence()
    updated_tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    updated_quote = update_random_quote(
        db, retrieved_quote=retrieved_quote, text=updated_text, tags=updated_tags
    )
    assert updated_quote.text == updated_text
    assert updated_quote.tags == updated_tags
    assert updated_quote.id == retrieved_quote.id


def test_update_quote_author(db: Session):
    text = _fake.sentence()
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    created_quote = create_random_quote(db, text=text, tags=tags)
    retrieved_quote = crud.quote.get(db, id=created_quote.id)
    assert retrieved_quote.text == text
    assert retrieved_quote.tags == tags

    updated_text = _fake.sentence()
    updated_tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    updated_quote, created_author = update_random_quote_with_random_author(
        db, retrieved_quote=retrieved_quote, text=updated_text, tags=updated_tags
    )
    assert updated_quote.text == updated_text
    assert updated_quote.tags == updated_tags
    assert updated_quote.id == retrieved_quote.id
    assert updated_quote.authors == created_author
    assert retrieved_quote.authors == created_author


def test_update_quote_with_random_author_and_categories(db: Session):
    text = _fake.sentence()
    tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"

    created_result = create_random_quote_with_random_author_and_category(
        db, text=text, tags=tags
    )
    created_quote, created_author, created_cat1, created_cat2 = created_result
    retrieved_quote = crud.quote.get(db, id=created_quote.id)
    assert retrieved_quote.text == text
    assert retrieved_quote.tags == tags

    updated_text = _fake.sentence()
    updated_tags = f"{_fake.word()},{_fake.word()},{_fake.word()}"
    updated_result = update_random_quote_with_random_author_and_categories(
        db, retrieved_quote=retrieved_quote, text=updated_text, tags=updated_tags
    )

    updated_quote, updated_author, updated_cat1, updated_cat2 = updated_result

    assert updated_quote.text == updated_text
    assert updated_quote.tags == updated_tags
    assert updated_quote.id == retrieved_quote.id
    assert updated_quote.authors == updated_author
    assert updated_cat1 in updated_quote.categories
    assert updated_cat2 in updated_quote.categories


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


def test_user_like_quote(db: Session):
    quote_in = QuoteCreate(
        text=_fake.sentence(), tags="word", categories_id=1, author_id=1
    )
    quote = crud.quote.create(db, obj_in=quote_in)
    user = UserCreate(name=_fake.name(), email=_fake.email(), password="Test123!")
    user = crud.user.create(db, obj_in=user)
    crud.quote.like(db, quote=quote, user=user)
    liked_quote = crud.quote.get(db, id=quote.id)
    assert user in liked_quote.users_who_liked


def test_user_unlike_quote(db: Session):
    quote_in = QuoteCreate(
        text=_fake.sentence(), tags="word", categories_id=1, author_id=1
    )
    quote = crud.quote.create(db, obj_in=quote_in)

    user = UserCreate(name=_fake.name(), email=_fake.email(), password="Test123!")
    user = crud.user.create(db, obj_in=user)

    crud.quote.like(db, quote=quote, user=user)
    crud.quote.unlike(db, quote=quote, user=user)
    unliked_quote = crud.quote.get(db, id=quote.id)
    assert user not in unliked_quote.users_who_liked
