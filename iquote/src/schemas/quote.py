from typing import List, Optional

from pydantic import BaseModel, ConfigDict

from schemas.categories import Categories as CategoriesSchema
from schemas.user import User as UserSchema


# Shared properties
class QuoteBase(BaseModel):
    text: str
    tags: Optional[str] = None
    author_id: Optional[int] = None
    categories: List[CategoriesSchema] = []


# Properties to receive via API on creation
class QuoteCreate(QuoteBase):
    categories: List[int] = []


# Properties to receive via API on update
class QuoteUpdate(QuoteBase):
    categories: List[int] = []


class QuoteInDBBase(QuoteBase):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Quote(QuoteInDBBase):
    users_who_liked: Optional[List[UserSchema]] = []
    liked_count: int = 0


class QuoteLike(Quote):
    liked: bool = False


class QuoteWithLike(Quote):
    users_who_liked: Optional[List[UserSchema]] = []
    liked_count: int = 0
    liked: bool = False


# Additional properties stored in DB
class QuoteInDB(QuoteInDBBase):
    pass
