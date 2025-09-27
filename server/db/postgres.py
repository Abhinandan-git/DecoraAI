from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config.env import NEON_URI

class PostgreSQL:
	engine = create_async_engine(NEON_URI, echo=True)
	SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
	Base = declarative_base()

	async def get_db(self):
		async with self.SessionLocal() as session:
			yield session
