from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from ..utils.auth import authenticate_user, create_access_token
from ..models.user import UserCreate, UserSignUp
from..models.generic import Token
from ..crud import users as user_crud

router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)

@router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(username=user["username"])
    return Token(access_token=access_token, token_type="bearer")


@router.post("/signup", response_model=UserSignUp, status_code=status.HTTP_201_CREATED)
async def signup(new_user: UserCreate):
    created_user = await user_crud.create_user(new_user.model_dump(by_alias=True, exclude=["id"]))
    return created_user