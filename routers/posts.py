from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.exceptions import ResponseValidationError, RequestValidationError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import PlainTextResponse, JSONResponse
from models.Post import Post
from utils.auth import TokenDepend, get_current_user, get_pass_hash, create_access_token,verify_password, user_data_valid, AuthUserDepend
from db import engine, SessionDep
from sqlmodel import select,col
from schemas.PostSchema import PostSchema, PostResponseSchema
from schemas.UserSchema import UserSchema, UserResponseSchema

from typing_extensions import List
from models.User import User
from typing_extensions import Annotated



router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('/', response_model=List[PostResponseSchema])
def get_posts(session:SessionDep, user:AuthUserDepend, limit:int=10, skip:int=0, search:str=''):

    stmt = select(Post)
    if len(search):
        stmt = stmt.where(col(Post.title).icontains(search))
    stmt = stmt.offset(skip).limit(limit)
    posts = session.exec(stmt).all()

    return posts


@router.get('/{id}')
def get_post(id: int,session:SessionDep):  
    stmt = select(Post, User).join(User, isouter=True).where(col(Post.id) == id)
    post = session.exec(stmt).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Post with id {id} not found")
    print('selected post', post)
    return post

@router.post('/')
def create_post(post: Post, response: Response, session:SessionDep, user: AuthUserDepend):
    post.owner_id = user.id
    session.add(post)
    session.commit()
    response.status_code = status.HTTP_201_CREATED
    return {"status": "ok", "message": f"post {post.title} has been created"}

@router.patch('/{id}', response_model=PostSchema)
def update_post(id: int,session:SessionDep, response: Response, post_body:Post):  
    stmt = select(Post).where(col(Post.id) == id)
    post:Post = session.exec(stmt).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            f"Post with id {id} not found")
                        
    post_body_dict = post_body.dict()
    
    for key, val in post_body_dict.items():        
        if hasattr(post, key):
            setattr(post, key, val)
    post.id = id
    

    try:
        session.add(post)
        session.commit()
        session.refresh(post)
    except Exception as e:
        session.rollback()

    return post



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, session:SessionDep, response: Response):

    post = session.get(Post,id) 
    session.delete(post)
    session.commit()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {id} not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)
