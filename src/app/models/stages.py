from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class Stage(base):
    __tablename__ = 'stages'

    id = Column(UUID, primary_key=True, default=uuid4)
    proc_id = Column(UUID, ForeignKey('processes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    is_start = Column(Boolean, default=False)
    is_end = Column(Boolean, default=False)
    duration = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Stage #{self.name}>"