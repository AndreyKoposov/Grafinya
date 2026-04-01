from typing import Optional
from uuid import uuid4
from uuid import UUID as ID
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy import select, insert, update, delete
from sqlalchemy.dialects.postgresql import UUID

from src.app.db.engine import base


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


    @staticmethod
    async def get_by_id(session: AsyncSession, param_id: ID) -> Optional['Parameter']:
        query = select(Parameter).where(Parameter.id == param_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_proc_id(session: AsyncSession, proc_id: ID) -> list['Parameter']:
        query = select(Parameter).where(Parameter.proc_id == proc_id)
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def create(session: AsyncSession, param_id: ID, name: str,
                     value_type: str, measure: str,
                     max_val: Optional[str] = None,
                     min_val: Optional[str] = None):
        query = insert(Parameter).values(
            param_id=param_id, name=name,
            value_type=value_type, measure=measure,
            max_val=max_val, min_val=min_val
        )
        await session.execute(query)

    @staticmethod
    async def update(session: AsyncSession, param_id: ID, name: str,
                     value_type: str, measure: str,
                     max_val: Optional[str] = None,
                     min_val: Optional[str] = None):
        query = update(Parameter).where(Parameter.id==param_id)\
                .values(param_id=param_id, name=name,
                        value_type=value_type, measure=measure,
                        max_val=max_val, min_val=min_val)
        await session.execute(query)

    @staticmethod
    async def delete(session: AsyncSession, param_id: ID):
        query = delete(Parameter).where(Parameter.id==param_id)
        await session.execute(query)
