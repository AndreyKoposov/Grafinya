from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


class Process(base):
    __tablename__ = 'processes'

    id = Column(UUID, primary_key=True, default=uuid4)
    user_id = Column(UUID, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Process #{self.name}>"

class Entity(base):
    __tablename__ = 'entities'

    id = Column(UUID, primary_key=True, default=uuid4)
    proc_id = Column(UUID, ForeignKey('processes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    tag = Column(Enum('human', 'machine', name='entity_tag'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Entity #{self.name}>"

class Parameter(base):
    __tablename__ = 'params'

    id = Column(UUID, primary_key=True, default=uuid4)
    proc_id = Column(UUID, ForeignKey('processes.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(50), nullable=False, index=True)
    value_type = Column(Enum('string', 'int', 'decimal', name='value_type'), nullable=False)
    measure = Column(String(50), nullable=False)
    max_value = Column(String(50), nullable=True)
    min_value = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Parameter #{self.name}>"

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

class EntityInStage(base):
    __tablename__ = 'entity_stage'

    id = Column(UUID, primary_key=True, default=uuid4)
    entity_id = Column(UUID, ForeignKey('entities.id', ondelete='CASCADE'), nullable=False)
    stage_id = Column(UUID, ForeignKey('stages.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Entity in Stage #{self.id}>"

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

class Transition(base):
    __tablename__ = 'transition'

    id = Column(UUID, primary_key=True, default=uuid4)
    stage_from_id = Column(UUID, ForeignKey('stages.id', ondelete='CASCADE'), nullable=False)
    stage_to_id = Column(UUID, ForeignKey('stages.id', ondelete='CASCADE'), nullable=False)
    condition_param = Column(UUID, ForeignKey('params.id', ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Parameter in Stage #{self.id}>"
