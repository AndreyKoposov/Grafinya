from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class User(base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    orioks_id = Column(String(10), unique=True, nullable=True, index=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<User #{self.orioks_id}>"
