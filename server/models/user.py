from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from db.postgres import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    privilege_level = Column(Integer, default=100)
    created_at = Column(DateTime(timezone=True), default=func.now())
    last_login_at = Column(DateTime(timezone=True), default=func.now())
    profile_picture_url = Column(String, default=None)

    # canvas = relationship("Canvas", back_populates="user")
