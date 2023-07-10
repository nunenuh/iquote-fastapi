from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from db.base_class import Base
from models.user import likes

# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # TIMESTAMP is used here to store timezone aware datetimes
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(TIMESTAMP(timezone=True))

    # Soft delete column
    is_deleted = Column(Boolean, server_default=expression.false())
    quotes = relationship("Quote", back_populates="authors")


# Association table for the many-to-many relationship between Quote and Category
quote_category_table = Table(
    "quote_categories",
    Base.metadata,
    Column("quote_id", Integer, ForeignKey("quote.id")),
    Column("categories_id", Integer, ForeignKey("categories.id")),
)


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"))
    children = relationship("Categories")

    # TIMESTAMP is used here to store timezone aware datetimes
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(TIMESTAMP(timezone=True))

    # Soft delete column
    is_deleted = Column(Boolean, server_default=expression.false())
    quotes = relationship(
        "Quote",
        secondary=quote_category_table,
        back_populates="categories",
    )


class Quote(Base):
    __tablename__ = "quote"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    tags = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    authors = relationship("Author", back_populates="quotes")

    categories = relationship(
        "Categories",
        secondary=quote_category_table,
        back_populates="quotes",
    )

    # relationship to the "User" model through the "likes" association table
    users_who_liked = relationship(
        "User",
        secondary=likes,
        back_populates="liked_quotes",
    )

    # TIMESTAMP is used here to store timezone aware datetimes
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(TIMESTAMP(timezone=True))

    # Soft delete column
    is_deleted = Column(Boolean, server_default=expression.false())
