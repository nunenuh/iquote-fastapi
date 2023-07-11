from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


likes = Table(
    "user_like_quote",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("quote_id", ForeignKey("quote.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    # items = relationship("Item", back_populates="owner")

    liked_quotes = relationship(
        "Quote",
        secondary=likes,
        back_populates="users_who_liked",
    )
