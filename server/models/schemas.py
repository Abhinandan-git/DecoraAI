from pydantic import BaseModel, EmailStr

class RegisterUserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str

