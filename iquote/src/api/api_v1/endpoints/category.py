from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Category])
async def read_category(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    category = crud.category.get_multi(db, skip=skip, limit=limit)
    return category


@router.get("/{category_id}", response_model=schemas.Category)
async def read_category_by_id(
    category_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    category = crud.category.get(db, id=category_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return category


@router.get("/name/{category_name}", response_model=schemas.Category)
async def read_category_by_id(
    category_name: str,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    category = crud.category.get_by_name(db, name=category_name)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return category


@router.get("/parent/{category_id}", response_model=List[schemas.Category])
async def read_category_by_id(
    category_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    category = crud.category.get_by_parent_id(db, parent_id=category_id)
    return category


@router.post("/", response_model=schemas.Category)
async def create_category(
    *,
    db: Session = Depends(deps.get_db),
    category_in: schemas.CategoryCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    category = crud.category.get_by_name(db, name=category_in.name)
    if category:
        raise HTTPException(
            status_code=400,
            detail="The quote author with this name already exists in the system.",
        )
    category = crud.category.create(db, obj_in=category_in)
    return category


@router.put("/{category_id}", response_model=schemas.Category)
async def update_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    category_in: schemas.CategoryUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    category = crud.category.update(db, db_obj=category, obj_in=category_in)
    return category


@router.delete("/{category_id}", response_model=schemas.Category)
async def delete_category(
    *,
    db: Session = Depends(deps.get_db),
    category_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    category = crud.category.get(db, id=category_id)
    if not category:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    category = crud.category.remove(db, id=category_id)
    return category
