from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing_extensions import Optional, List
# from email_validator import 
# from fastapi import 

class User(SQLModel, table=True):
    __tablename__ = 'users'
    id:Optional[int] = Field(primary_key=True)
    email: EmailStr = Field(unique=True, nullable=False)
    password: str
    
    posts: List['Post'] = Relationship(back_populates='owner')