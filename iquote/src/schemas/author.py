from typing import Optional

from pydantic import BaseModel, ConfigDict


# Shared properties
class AuthorBase(BaseModel):
    name: str


# Properties to receive via API on creation
class AuthorCreate(AuthorBase):
    pass


# Properties to receive via API on update
class AuthorUpdate(AuthorBase):
    pass


class AuthorInDBBase(AuthorBase):
    id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


# Additional properties to return via API
class Author(AuthorInDBBase):
    pass


# Additional properties stored in DB
class AuthorInDB(AuthorInDBBase):
    pass
