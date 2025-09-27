from motor.motor_asyncio import AsyncIOMotorClient

# Import environment variables
from config.env import MONGO_URI

# Send a ping to confirm a successful connection
async def get_db():
	client = AsyncIOMotorClient(MONGO_URI)
	db = client["DecoraAI"]
	return db
