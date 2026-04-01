from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class Transition(base):
    __tablename__ = 'transition'

    id = Column(UUID, primary_key=True, default=uuid4)
    stage_from_id = Column(UUID, ForeignKey('stages.id', ondelete='CASCADE'), nullable=False)
    stage_to_id = Column(UUID, ForeignKey('stages.id', ondelete='CASCADE'), nullable=False)
    condition_param = Column(UUID, ForeignKey('params.id', ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Parameter in Stage #{self.id}>"