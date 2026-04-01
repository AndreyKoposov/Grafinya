from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class ParamInStage(base):
    __tablename__ = 'param_stage'

    id = Column(UUID, primary_key=True, default=uuid4)
    param_id = Column(UUID, ForeignKey('params.id', ondelete='CASCADE'), nullable=False)
    stage_id = Column(UUID, ForeignKey('stages.id', ondelete='CASCADE'), nullable=False)
    role = Column(Enum('input', 'control', 'resource', 'output', name='param_role'), nullable=False)
    value = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Parameter in Stage #{self.id}>"