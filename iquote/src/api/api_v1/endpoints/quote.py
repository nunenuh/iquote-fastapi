from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Quote])
async def read_quotes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve quotes.
    """
    quotes = crud.quote.get_multi(db, skip=skip, limit=limit)
    return quotes


@router.get("/{quote_id}", response_model=schemas.Quote)
async def read_quote_by_id(
    quote_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific quote by id.
    """
    quote = crud.quote.get(db, id=quote_id)
    return quote


@router.get("/by/author/{author_id}", response_model=schemas.Quote)
async def read_quote_by_author_id(
    author_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific quote by id.
    """
    quote = crud.quote.get_by_author_id(db, author_id=author_id)
    return quote


@router.get("/by/author/name/{author_name}", response_model=List[schemas.Quote])
async def read_quote_by_author_name(
    author_name: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific quote by id.
    """
    quote = crud.quote.get_by_author_name(db, author_name=author_name)
    return quote


@router.get("/by/categories/{categories_id}", response_model=schemas.Quote)
async def read_quote_by_categories_id(
    categories_id: int,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific quote by id.
    """
    quote = crud.quote.get_by_categories_id(db, categories_id=categories_id)
    return quote


@router.get("/by/categories/name/{categories_name}", response_model=List[schemas.Quote])
async def read_quote_by_categories_name(
    categories_name: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific quote by id.
    """
    quote = crud.quote.get_by_categories_name(db, categories_name=categories_name)
    return quote


@router.post("/", response_model=schemas.Quote)
async def create_quote(
    *,
    db: Session = Depends(deps.get_db),
    quote_in: schemas.QuoteCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote = crud.quote.create(db, obj_in=quote_in)
    return quote


# create for me servive for quote like
@router.put("/{quote_id}/like", response_model=schemas.QuoteWithLike)
async def like_quote(
    *,
    db: Session = Depends(deps.get_db),
    quote_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    quote = crud.quote.get(db, id=quote_id)
    if not quote:
        raise HTTPException(
            status_code=404,
            detail="The quote with this id does not exist in the system",
        )
    quote = crud.quote.like(db, quote=quote, user=current_user)
    return quote


@router.put("/{quote_id}/unlike", response_model=schemas.QuoteWithLike)
async def unlike_quote(
    *,
    db: Session = Depends(deps.get_db),
    quote_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    quote = crud.quote.get(db, id=quote_id)
    if not quote:
        raise HTTPException(
            status_code=404,
            detail="The quote with this id does not exist in the system",
        )
    quote = crud.quote.unlike(db, quote=quote, user=current_user)
    return quote


@router.put("/{quote_id}", response_model=schemas.Quote)
async def update_quote(
    *,
    db: Session = Depends(deps.get_db),
    quote_id: int,
    quote_in: schemas.QuoteUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote = crud.quote.get(db, id=quote_id)
    if not quote:
        raise HTTPException(
            status_code=404,
            detail="The quote with this id does not exist in the system",
        )
    quote = crud.quote.update(db, db_obj=quote, obj_in=quote_in)
    return quote


@router.delete("/{quote_id}", response_model=schemas.Quote)
async def delete_quote(
    *,
    db: Session = Depends(deps.get_db),
    quote_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote = crud.quote.get(db, id=quote_id)
    if not quote:
        raise HTTPException(
            status_code=404,
            detail="The quote with this id does not exist in the system",
        )
    quote = crud.quote.remove(db, id=quote_id)
    return quote
