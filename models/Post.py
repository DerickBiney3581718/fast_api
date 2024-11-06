from typing import Optional
from sqlmodel import Field, SQLModel, Relationship
from typing_extensions import Annotated
from fastapi import Query
from datetime import datetime
from models.User import User

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Annotated[str, Query(min_length=10)]
    published: bool
    rating: Optional[float]
    created_at:datetime =  Field(nullable=True, default=datetime.now())
    owner_id: Optional[int] = Field(default=None, foreign_key='users.id')

    owner:Optional[User] = Relationship(back_populates='posts')