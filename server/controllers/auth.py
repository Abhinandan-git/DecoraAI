from fastapi import APIRouter, Depends
from typing import Annotated
from uuid import UUID

# Remove this import
from uuid import uuid4

from server.db.postgres import get_db

from server.models.postgres import RegisterUserModel, LoginUserModel

router = APIRouter(prefix="/api/v1")

@router.post("/register")
def register_user(user: Annotated[RegisterUserModel, Depends(get_db)]):
	# Get the user from database

	# Check if user exists, return fail

	# Else, create the user using UserModel

	# Remove this and return user_id created
	pass

@router.post("/login")
def login_user(user: Annotated[LoginUserModel, Depends(get_db)]):
	# Get the user from database

	# Check if user does not exists, return fail

	# Else, retrieve and return token

	# Remove this and return user_id/token created
	pass
