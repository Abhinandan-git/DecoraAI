import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv("SECRET", "")
ALGORITHM = os.getenv("ALGO", "")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
MONGO_URI = os.getenv("MONGO_URI", "")
NEON_URI = os.getenv("NEON_URI", "")