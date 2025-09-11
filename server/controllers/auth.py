from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server.db.postgres import get_db

from server.models.postgres import RegisterUserModel, LoginUserModel
from server.models.user import User

router = APIRouter(prefix="/api/v1")

@router.post("/register")
async def register_user(user: RegisterUserModel, database: Session = Depends(get_db)):
	# Get the user from database

	# Check if user exists, return fail

	# Else, create the user using UserModel

	# Remove this and return user_id created
	pass

@router.post("/login")
async def login_user(user: LoginUserModel, database: Session = Depends(get_db)):
	# Get the user from database
	db_user = database.query(User).filter(User.username == user.username).first()
	return db_user

	# Check if user does not exists, return fail

	# Else, retrieve and return token

	# Remove this and return user_id/token created
	pass
