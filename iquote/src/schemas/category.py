from typing import Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None


# Properties to receive via API on creation
class CategoryCreate(CategoryBase):
    pass


# Properties to receive via API on update
class CategoryUpdate(CategoryBase):
    pass


class CategoryInDBBase(CategoryBase):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Category(CategoryInDBBase):
    pass


# Additional properties stored in DB
class CategoryInDB(CategoryInDBBase):
    pass
