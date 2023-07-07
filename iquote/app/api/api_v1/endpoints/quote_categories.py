from typing import Any, List

import crud
import models
import schemas
from api import deps
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", response_model=List[schemas.QuoteCategories])
def read_quote_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    quote_categoriess = crud.quote_categories.get_multi(db, skip=skip, limit=limit)
    return quote_categoriess


@router.get("/{category_id}", response_model=schemas.QuoteCategories)
def read_quote_categories_by_id(
    category_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    quote_categories = crud.quote_categories.get(db, id=category_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return quote_categories


@router.get("/name/{category_name}", response_model=schemas.QuoteCategories)
def read_quote_categories_by_id(
    category_name: str,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    quote_categories = crud.quote_categories.get_by_name(db, name=category_name)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return quote_categories


@router.get("/parent/id/{category_id}", response_model=schemas.QuoteCategories)
def read_quote_categories_by_id(
    category_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    quote_categories = crud.quote_categories.get_by_parent_id(db, parent_id=category_id)
    return quote_categories


@router.post("/", response_model=schemas.QuoteCategories)
def create_quote_categories(
    *,
    db: Session = Depends(deps.get_db),
    quote_categories_in: schemas.QuoteCategoriesCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote_categories = crud.quote_categories.get_by_name(
        db, name=quote_categories_in.name
    )
    if quote_categories:
        raise HTTPException(
            status_code=400,
            detail="The quote author with this name already exists in the system.",
        )
    quote_categories = crud.quote_categories.create(db, obj_in=quote_categories_in)
    return quote_categories


@router.put("/{category_id}", response_model=schemas.QuoteCategories)
def update_quote_categories(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    quote_categories_in: schemas.QuoteCategoriesUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote_categories = crud.quote_categories.get(db, id=category_id)
    if not quote_categories:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    quote_categories = crud.quote_categories.update(
        db, db_obj=quote_categories, obj_in=quote_categories_in
    )
    return quote_categories


@router.delete("/{category_id}", response_model=schemas.QuoteCategories)
def delete_quote_categories(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    quote_categories = crud.quote_categories.get(db, id=category_id)
    if not quote_categories:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    quote_categories = crud.quote_categories.remove(db, id=category_id)
    return quote_categories
