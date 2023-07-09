from db.base_class import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship


class QuoteAuthor(Base):
    __tablename__ = "quote_author"

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


class QuoteCategories(Base):
    __tablename__ = "quote_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("quote_categories.id"))
    children = relationship("QuoteCategories")

    # TIMESTAMP is used here to store timezone aware datetimes
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(TIMESTAMP(timezone=True))

    # Soft delete column
    is_deleted = Column(Boolean, server_default=expression.false())
    quotes = relationship("Quote", back_populates="categories")


class Quote(Base):
    __tablename__ = "quote"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    tags = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("quote_author.id"))
    authors = relationship("QuoteAuthor", back_populates="quotes")
    categories_id = Column(Integer, ForeignKey("quote_categories.id"))
    categories = relationship("QuoteCategories", back_populates="quotes")

    # TIMESTAMP is used here to store timezone aware datetimes
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(TIMESTAMP(timezone=True))

    # Soft delete column
    is_deleted = Column(Boolean, server_default=expression.false())
