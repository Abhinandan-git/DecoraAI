from uuid import UUID, uuid4
from typing import List
from datetime import datetime

class UserModel:
    user_id: UUID = uuid4()
    username: str
    email: str
    password: str
    priviledge_level: int = 100
    created_at: datetime = datetime.now()
    last_login: datetime
    profile_picture_url: str = ""
    canvases: List[UUID] = []
