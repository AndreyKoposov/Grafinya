from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, Text, Enum, ForeignKey, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class Messages(base):
    __tablename__ = 'messages'

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'))
    text = Column(Text, nullable=False)
    sender = Column(Enum('user', 'ai', name='sender'), nullable=False)
    read = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now)


    def __repr__(self) -> str:
        return f"<Message {self.id}>"
