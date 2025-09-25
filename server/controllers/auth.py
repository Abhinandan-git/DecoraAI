from fastapi import APIRouter, Depends, HTTPException

from db.postgres import get_db as database
from models.user import User
from models.schemas import RegisterUserSchema, LoginUserSchema
from utils.generateToken import create_access_token

from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter(prefix="/api/v1")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(user: RegisterUserSchema, db: AsyncSession = Depends(database)):
    result = await db.execute(select(User).where(
        (User.email == user.email) | (User.username == user.username)
    ))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = pwd_context.hash(user.password)
 
    db_user = User(username=user.username, email=user.email, password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    access_token = create_access_token(data={"sub": str(db_user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login")
async def login_user(user: LoginUserSchema, db: AsyncSession = Depends(database)):
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalars().first()
    
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not pwd_context.verify(user.password, str(db_user.password)):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": str(db_user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}
