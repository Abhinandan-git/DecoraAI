from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid

from db.postgres import Base

class Canvas(Base):
    __tablename__ = "canvas"

    room_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    custom_code = Column(String, unique=True, nullable=True, default="")
    canvas_name = Column(String, unique=True)
    description = Column(String, nullable=True, default="")
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

    user = relationship("User", back_populates="canvas")
