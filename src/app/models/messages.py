from uuid import uuid4
from datetime import datetime, timezone
from sqlalchemy import Column, String, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class Messages(base):
    __tablename__ = 'messages'

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'))
    text = Column(String(500), nullable=False)
    sender = Column(Enum('user', 'ai', name='sender'), nullable=False)
    read = Column(Boolean)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


    def __repr__(self) -> str:
        return f"<Message {self.id}>"
