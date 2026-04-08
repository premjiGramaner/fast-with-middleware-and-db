from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from .database import Base

# DB Model


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    password = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, index=True)
