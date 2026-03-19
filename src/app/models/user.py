from sqlalchemy import Column, String, DateTime
from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    name = Column(String(20), unique=True, nullable=False, index=True)
    orioks_id = Column(String(10), unique=True, nullable=True, index=True)
    last_login = Column(DateTime, nullable=True)
