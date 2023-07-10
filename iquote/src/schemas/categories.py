from typing import Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class CategoriesBase(BaseModel):
    name: str


# Properties to receive via API on creation
class CategoriesCreate(CategoriesBase):
    pass


# Properties to receive via API on update
class CategoriesUpdate(CategoriesBase):
    pass


class CategoriesInDBBase(CategoriesBase):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Categories(CategoriesInDBBase):
    pass


# Additional properties stored in DB
class CategoriesInDB(CategoriesInDBBase):
    pass
