from typing import Optional

from pydantic import BaseModel


# Shared properties
class QuoteCategoriesBase(BaseModel):
    name: str


# Properties to receive via API on creation
class QuoteCategoriesCreate(QuoteCategoriesBase):
    pass


# Properties to receive via API on update
class QuoteCategoriesUpdate(QuoteCategoriesBase):
    pass


class QuoteCategoriesInDBBase(QuoteCategoriesBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class QuoteCategories(QuoteCategoriesInDBBase):
    pass


# Additional properties stored in DB
class QuoteCategoriesInDB(QuoteCategoriesInDBBase):
    pass
