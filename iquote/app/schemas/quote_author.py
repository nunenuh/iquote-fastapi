from typing import Optional

from pydantic import BaseModel


# Shared properties
class QuoteAuthorBase(BaseModel):
    name: str


# Properties to receive via API on creation
class QuoteAuthorCreate(QuoteAuthorBase):
    pass


# Properties to receive via API on update
class QuoteAuthorUpdate(QuoteAuthorBase):
    pass


class QuoteAuthorInDBBase(QuoteAuthorBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class QuoteAuthor(QuoteAuthorInDBBase):
    pass


# Additional properties stored in DB
class QuoteAuthorInDB(QuoteAuthorInDBBase):
    pass
