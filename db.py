from config import load_config
from typing import Optional, List, Union
from typing_extensions import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select, MetaData

config = load_config()
db_url = f"postgresql+psycopg2://{config['username']}:{config['password']}@{config['host']}/{config['database']}"

# connect_args = {"check_same_thread": False}
engine = create_engine(db_url)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
