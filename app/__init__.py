from models.Post import Post
from models.User import User
from db import engine
from sqlmodel import SQLModel

SQLModel.metadata.create_all(engine)
            