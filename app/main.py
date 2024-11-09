from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.exceptions import ResponseValidationError, RequestValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import PlainTextResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from models.Post import Post
from utils.auth import TokenDepend, get_current_user, get_pass_hash, create_access_token,verify_password, user_data_valid
from db import engine, SessionDep
from sqlmodel import select,col
from schemas.PostSchema import PostSchema
from schemas.UserSchema import UserSchema, UserResponseSchema
from routers import auth, posts
from typing_extensions import List
from models.User import User
from typing_extensions import Annotated

app = FastAPI()


origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ResponseValidationError)
async def response_validation_handler(req, exc):
    return JSONResponse({'errors':str(exc)}, status_code=500)

@app.exception_handler(RequestValidationError)
async def request_validation_handler(req, exc):
    return JSONResponse({'errors':str(exc)}, status_code=400)

app.include_router(auth.router)
app.include_router(posts.router)

@app.get('/')   
async def root():
    return {'message':'hello world'}

# Godaddy, A2, 