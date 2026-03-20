from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class User(base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid4)
    name = Column(String(20), unique=True, nullable=False, index=True)
    orioks_id = Column(String(10), unique=False, nullable=True, index=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.name}>"
