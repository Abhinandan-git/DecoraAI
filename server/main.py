from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.mongo_database import ping_mongo_database
from utils.postgres_database import get_postgres_database
app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_credentials=True,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

ping_mongo_database()
get_postgres_database()

@app.get("/")
def read_root():
	return {"message": "Hello, World!"}
