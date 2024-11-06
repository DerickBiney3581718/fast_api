from typing import Optional
from typing_extensions import Annotated
from fastapi import Query
from pydantic import BaseModel, EmailStr
from datetime import datetime
from .UserSchema import UserResponseSchema
class PostSchema(BaseModel):
    title: Annotated[str, Query(min_length=10)]
    published: bool
    rating: Optional[float]
    created_at: datetime
    

class PostResponseSchema(BaseModel):
    title: Annotated[str, Query(min_length=10)]
    published: bool
    rating: Optional[float]
    created_at: datetime
    owner_id:Optional[int]
    owner:Optional[UserResponseSchema]