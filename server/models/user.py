from sqlalchemy import Column, Integer, String, DateTime, func

from server.db.postgres import Base

class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True, nullable=True)
	email = Column(String, unique=True, index=True, nullable=False)
	password = Column(String, nullable=False)
	created_at = Column(DateTime(timezone=True), server_default=func.now())
