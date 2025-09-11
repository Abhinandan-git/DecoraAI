from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.controllers.auth import router as auth_router

app = FastAPI()

app.add_middleware(
	CORSMiddleware,
	allow_credentials=True,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
async def read_root():
	return {"message": "Hello, World!"}
