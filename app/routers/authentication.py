from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta
from ..utils.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRES_MINUTES, create_user
from ..models.user import User, UserCreate, Token, UserSignUp

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request
) -> Token:
    user = await authenticate_user(request.app.database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    access_token = create_access_token(
        data={"sub": user["user_name"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup", response_model=UserSignUp, status_code=status.HTTP_201_CREATED)
async def signup(request: Request, new_user: UserCreate):
    created_user = await create_user(request.app.database, new_user.model_dump())
    return created_user