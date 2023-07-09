from typing import Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class QuoteBase(BaseModel):
    text: str
    tags: Optional[str] = None
    author_id: Optional[int] = None
    categories_id: Optional[int] = None


# Properties to receive via API on creation
class QuoteCreate(QuoteBase):
    pass


# Properties to receive via API on update
class QuoteUpdate(QuoteBase):
    pass


class QuoteInDBBase(QuoteBase):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Quote(QuoteInDBBase):
    pass


# Additional properties stored in DB
class QuoteInDB(QuoteInDBBase):
    pass
