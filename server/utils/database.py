from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Import environment variables
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("MONGO_URI", "")

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
def ping_database():
	try:
		client.admin.command("ping")
		print("Pinged your deployment. You successfully connected to MongoDB!")
	except Exception as e:
		print(e)

# Return the collection instance to the caller
def get_collection():
	return client.DecoraAI.canvas
