from typing import Any, List

import crud
import models
import schemas
from api import deps
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[schemas.QuoteAuthor])
def read_quote_author(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    quote_authors = crud.quote_author.get_multi(db, skip=skip, limit=limit)
    return quote_authors


@router.get("/{author_id}", response_model=schemas.QuoteAuthor)
def read_user_by_id(
    author_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    quote_author = crud.quote_author.get(db, id=author_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return quote_author


@router.post("/", response_model=schemas.QuoteAuthor)
def create_quote_author(
    *,
    db: Session = Depends(deps.get_db),
    quote_author_in: schemas.QuoteAuthorCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote_author = crud.quote_author.get_by_name(db, name=quote_author_in.name)
    if quote_author:
        raise HTTPException(
            status_code=400,
            detail="The quote author with this name already exists in the system.",
        )
    quote_author = crud.quote_author.create(db, obj_in=quote_author_in)
    return quote_author


@router.put("/{author_id}", response_model=schemas.QuoteAuthor)
def update_quote_author(
    *,
    db: Session = Depends(deps.get_db),
    author_id: int,
    quote_author_in: schemas.QuoteAuthorUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote_author = crud.quote_author.get(db, id=author_id)
    if not quote_author:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    quote_author = crud.quote_author.update(
        db, db_obj=quote_author, obj_in=quote_author_in
    )
    return quote_author


@router.delete("/{author_id}", response_model=schemas.QuoteAuthor)
def delete_quote_author(
    *,
    db: Session = Depends(deps.get_db),
    author_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote_author = crud.quote_author.get(db, id=author_id)
    if not quote_author:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    quote_author = crud.quote_author.remove(db, id=author_id)
    return quote_author
