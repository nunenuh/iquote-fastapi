from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.Author])
def read_author(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    authors = crud.author.get_multi(db, skip=skip, limit=limit)
    return authors


@router.get("/{author_id}", response_model=schemas.Author)
def read_author_by_id(
    author_id: int,
    # current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    author = crud.author.get(db, id=author_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return author


@router.post("/", response_model=schemas.Author)
def create_author(
    *,
    db: Session = Depends(deps.get_db),
    author_in: schemas.AuthorCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    author = crud.author.get_by_name(db, name=author_in.name)
    if author:
        raise HTTPException(
            status_code=400,
            detail="The quote author with this name already exists in the system.",
        )
    author = crud.author.create(db, obj_in=author_in)
    return author


@router.put("/{author_id}", response_model=schemas.Author)
def update_author(
    *,
    db: Session = Depends(deps.get_db),
    author_id: int,
    author_in: schemas.AuthorUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    author = crud.author.get(db, id=author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    author = crud.author.update(db, db_obj=author, obj_in=author_in)
    return author


@router.delete("/{author_id}", response_model=schemas.Author)
def delete_author(
    *,
    db: Session = Depends(deps.get_db),
    author_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    author = crud.author.get(db, id=author_id)
    if not author:
        raise HTTPException(
            status_code=404,
            detail="The quote author with this id does not exist in the system",
        )
    author = crud.author.remove(db, id=author_id)
    return author
