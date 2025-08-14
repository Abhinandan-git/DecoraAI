from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import json

import utils.database

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_credentials=True,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

utils.database.ping_database()

@app.get("/")
def read_root():
	return {"message": "Hello, World!"}
