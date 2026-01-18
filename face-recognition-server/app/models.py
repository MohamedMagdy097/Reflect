from sqlalchemy import Column, Integer, String, JSON, DateTime, Index, func
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    embedding = Column(JSON, nullable=False)  # Store as JSON array
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Index for faster lookups
    __table_args__ = (
        Index("idx_email", "email"),
    )
