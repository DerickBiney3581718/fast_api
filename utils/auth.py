
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated, Union, Dict
from db import SessionDep
from sqlmodel import select,col

from passlib.context import CryptContext
from models.User import User
from datetime import timedelta, datetime
from jwt import encode, decode, PyJWTError
from config import load_jwt_config
from schemas.UserSchema import UserSchema
from pydantic import BaseModel, EmailStr


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token') #this is the signup, take user cred -> token | setting token endpoint of the auth server

TokenDepend = Annotated[str, Depends(oauth2_scheme)]

form_data =  Annotated[OAuth2PasswordRequestForm, Depends()]

class Token(BaseModel):
    access_token:str
    token_type:str

def get_current_user(form_data:form_data, session:SessionDep):
    stmt = select(User).where(User.email==form_data.username)
    user = None
    try: 
        user = session.exec(stmt).one()
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'User was not found')
    return user

def get_user_by_id(id:str, db:SessionDep):
    user=None
    try:
        stmt = db.get(User,id)
        user = stmt.exec()
    except Exception as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Invalid credentials')
    return user

def get_user_by_email(email:EmailStr, db:SessionDep):
    user = None

    try:
        user = db.exec(select(User).where(User.email==email)).one()
        print('user from get email', user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid credentials {str(e)}')
    return user
pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pass_context.verify(plain_password, hashed_password)

def get_pass_hash(plain_password):
    return pass_context.hash(plain_password)

def create_access_token(data:Dict, expires_delta: Union[timedelta, None]=None)->Token:
    config = load_jwt_config()
    payload = data.copy()

    print('payload', payload)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else: 
        expire = datetime.utcnow() + timedelta(minutes=15)

    
    payload.update({'exp':expire})

    access_token =  encode(payload, key=config['secret_key'], algorithm=config['algorithm'])
    return Token(access_token=access_token, token_type = 'bearer')

def user_data_valid(user_data:Annotated[UserSchema, Depends()]):
    return User(**user_data)

def authenticate_user(token:TokenDepend, db:SessionDep):
    config = load_jwt_config()

    user = None

    try:
        payload = decode(token, key=config.get('secret_key'), algorithms=[config.get('algorithm')])

        user_id = payload.get('user_id')
        print('user id from payload', user_id)
        user = get_user_by_email(user_id, db)

        if not user:
            raise HTTPException(status.HTTP_403_FORBIDDEN, f'Invalid credentials - no user found')

    except PyJWTError as e:
        raise HTTPException(status.HTTP_403_FORBIDDEN, f'Invalid credentials {str(e)}')
    return user

AuthUserDepend = Annotated[User, Depends(authenticate_user)]