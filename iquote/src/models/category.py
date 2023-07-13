from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from db.base_class import Base
from models.quote import quote_category_table


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey("category.id"))
    children = relationship("Category")
    quotes = relationship(
        "Quote",
        secondary=quote_category_table,
        back_populates="categories",
    )

    # TIMESTAMP is used here to store timezone aware datetimes
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    deleted_at = Column(TIMESTAMP(timezone=True))

    # Soft delete column
    is_deleted = Column(Boolean, server_default=expression.false())
