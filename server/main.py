from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.db.mongo import get_db as get_mongo_db
from server.db.postgres import get_db as get_postgres_db

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_credentials=True,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

@app.get("/")
async def read_root():
	return {"message": "Hello, World!"}
