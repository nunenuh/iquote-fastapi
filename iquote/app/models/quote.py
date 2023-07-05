from db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String, func
from sqlalchemy.dialects.postgresql import TIMESTAMP
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
