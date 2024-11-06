from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.exceptions import ResponseValidationError, RequestValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import PlainTextResponse, JSONResponse
from models.Post import Post
from utils.auth import TokenDepend, get_current_user, get_pass_hash, create_access_token,verify_password, user_data_valid

from db import engine, SessionDep
from sqlmodel import select,col
from schemas.PostSchema import PostSchema
from schemas.UserSchema import UserSchema, UserResponseSchema

from typing_extensions import List
from models.User import User
from typing_extensions import Annotated

router = APIRouter(tags=["Auth"])

@router.post("/token")
def login(credentials: Annotated[OAuth2PasswordRequestForm, Depends()], user : Annotated[UserSchema, Depends(get_current_user)]):
    if not verify_password(credentials.password, user.password):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, 'Invalid credentials')
    return create_access_token({'user_id': credentials.username})
    # OAuth

@router.post('/signup', response_model=UserResponseSchema)
def signup( credentials: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep,):
    hashed_password = get_pass_hash(credentials.password)
    user= user_data_valid({'password': hashed_password, 'email':credentials.username})
    try:
        session.add(user)
        session.commit()
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))
    session.refresh(user)
    return user