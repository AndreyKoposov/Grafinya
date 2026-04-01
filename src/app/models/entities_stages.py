from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class EntityInStage(base):
    __tablename__ = 'entity_stage'

    id = Column(UUID, primary_key=True, default=uuid4)
    entity_id = Column(UUID, ForeignKey('entities.id', ondelete='CASCADE'), nullable=False)
    stage_id = Column(UUID, ForeignKey('stages.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Entity in Stage #{self.id}>"