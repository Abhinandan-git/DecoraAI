from motor.motor_asyncio import AsyncIOMotorClient

# Import environment variables
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")

# Send a ping to confirm a successful connection
async def get_db():
	client = AsyncIOMotorClient("mongodb://localhost:27017")
	db = client["mydatabase"]
	return db
