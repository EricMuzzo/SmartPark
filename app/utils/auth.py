from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from motor.motor_asyncio import AsyncIOMotorDatabase
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from ..models.user import User, UserCreate, Token, TokenData
from ..schemas.user import user_serial
import os

#Possible solution to passlib bcrypt dependency issue: https://github.com/pyca/bcrypt/issues/684#issuecomment-1902590553

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRES_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")
    
    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db: AsyncIOMotorDatabase, username: str):
    document = await db["users"].find_one({"user_name": username})
    if document:
        return document
    return None

    
async def authenticate_user(db: AsyncIOMotorDatabase, username: str, password: str) -> User:
    user = await get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user["password"]):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncIOMotorDatabase
) -> UserCreate:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_name: str = payload.get("sub")
        if user_name is None:
            raise credentials_exception
        token_data = TokenData(user_name=user_name)
    except InvalidTokenError:
        raise credentials_exception
    

    user = await get_user(db=db, username=token_data.user_name)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserCreate, Depends(get_current_user)],
) -> UserCreate:
    print("User:", current_user)
    return current_user

async def create_user(db: AsyncIOMotorDatabase, user_data: dict) -> dict:
    # Check if a user with the given username already exists
    existing_user = await get_user(db, user_data["user_name"])
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    # Hash the password and remove the plain-text version
    user_data["password"] = get_password_hash(user_data["password"])
    result = await db["users"].insert_one(user_data)
    new_user = await db["users"].find_one({"_id": result.inserted_id})
    if new_user is None:
        raise HTTPException(status_code=500, detail="User creation failed")
    
    serialized_new_user = user_serial(new_user)
    
    #Get an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    token = create_access_token(
        data={"sub": new_user["user_name"]}, expires_delta=access_token_expires
    )
    
    serialized_new_user["token"] = Token(access_token=token, token_type="bearer")
    return serialized_new_user