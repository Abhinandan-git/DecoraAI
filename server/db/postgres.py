from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

NEON_URI = os.getenv("NEON_URI", "")

async def get_db():
	engine = create_async_engine(NEON_URI, echo=True)
	SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
	Base = declarative_base()

	async with SessionLocal() as session:
		yield session
