from uuid import UUID, uuid4
from typing import List
from datetime import datetime
from pydantic import BaseModel

class RegisterUserModel(BaseModel):
    user_id: UUID = uuid4()
    username: str
    email: str
    password: str
    priviledge_level: int = 100
    created_at: datetime = datetime.now()
    last_login: datetime
    profile_picture_url: str = ""
    canvases: List[UUID] = []

class LoginUserModel(BaseModel):
    username: str
    email: str
    password: str
