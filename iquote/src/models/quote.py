from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    func,
    select,
)
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from db.base_class import Base
from models.user import user_like_quote

# Association table for the many-to-many relationship between Quote and Category
quote_category_table = Table(
    "quote_category",
    Base.metadata,
    Column("quote_id", Integer, ForeignKey("quote.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)


class Quote(Base):
    __tablename__ = "quote"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    tags = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("author.id"))
    authors = relationship("Author", back_populates="quotes")

    categories = relationship(
        "Category",
        secondary=quote_category_table,
        back_populates="quotes",
    )

    # relationship to the "User" model through the "likes" association table
    users_who_liked = relationship(
        "User",
        secondary=user_like_quote,
        back_populates="liked_quotes",
    )

    @hybrid_property
    def liked_count(self):
        return len(self.users_who_liked)

    @liked_count.expression
    def liked_count(cls):
        return (
            select([func.count(user_like_quote.c.user_id)])
            .where(user_like_quote.c.quote_id == cls.id)
            .label("liked_count")
        )

    # TIMESTAMP is used here to store timezone aware datetimes
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(TIMESTAMP(timezone=True))

    # Soft delete column
    is_deleted = Column(Boolean, server_default=expression.false())
