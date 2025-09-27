from motor.motor_asyncio import AsyncIOMotorClient

# Import environment variables
from config.env import MONGO_URI

# Send a ping to confirm a successful connection
class MongoDB:
	uri: str = MONGO_URI

	async def get_db(self):
		client = AsyncIOMotorClient(self.uri)
		db = client["DecoraAI"]
		return db
