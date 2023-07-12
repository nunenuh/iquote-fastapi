from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Categories])
def read_categories(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    categories = crud.categories.get_multi(db, skip=skip, limit=limit)
    return categories


@router.get("/{category_id}", response_model=schemas.Categories)
def read_categories_by_id(
    category_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    categories = crud.categories.get(db, id=category_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return categories


@router.get("/name/{category_name}", response_model=schemas.Categories)
def read_categories_by_id(
    category_name: str,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    categories = crud.categories.get_by_name(db, name=category_name)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return categories


@router.get("/parent/{category_id}", response_model=List[schemas.Categories])
def read_categories_by_id(
    category_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    categories = crud.categories.get_by_parent_id(db, parent_id=category_id)
    return categories


@router.post("/", response_model=schemas.Categories)
def create_categories(
    *,
    db: Session = Depends(deps.get_db),
    categories_in: schemas.CategoriesCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    categories = crud.categories.get_by_name(db, name=categories_in.name)
    if categories:
        raise HTTPException(
            status_code=400,
            detail="The quote author with this name already exists in the system.",
        )
    categories = crud.categories.create(db, obj_in=categories_in)
    return categories


@router.put("/{category_id}", response_model=schemas.Categories)
def update_categories(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    categories_in: schemas.CategoriesUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    categories = crud.categories.get(db, id=category_id)
    if not categories:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    categories = crud.categories.update(db, db_obj=categories, obj_in=categories_in)
    return categories


@router.delete("/{category_id}", response_model=schemas.Categories)
def delete_categories(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    categories = crud.categories.get(db, id=category_id)
    if not categories:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    categories = crud.categories.remove(db, id=category_id)
    return categories
