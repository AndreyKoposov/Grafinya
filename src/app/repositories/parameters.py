from typing import Optional
from uuid import UUID
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.app.models.process import Parameter


class ParamRepo():
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, param_id: UUID) -> Optional[Parameter]:
        query = select(Parameter).where(Parameter.id == param_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_proc_id(self, proc_id: UUID) -> list[Parameter]:
        query = select(Parameter).where(Parameter.proc_id == proc_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, param_id: UUID, name: str,
                     value_type: str, measure: str,
                     max_val: Optional[str] = None,
                     min_val: Optional[str] = None):
        query = insert(Parameter).values(
            param_id=param_id, name=name,
            value_type=value_type, measure=measure,
            max_val=max_val, min_val=min_val
        )
        await self.session.execute(query)

    async def update(self, param_id: UUID, name: str,
                     value_type: str, measure: str,
                     max_val: Optional[str] = None,
                     min_val: Optional[str] = None):
        query = update(Parameter).where(Parameter.id==param_id)\
                .values(param_id=param_id, name=name,
                        value_type=value_type, measure=measure,
                        max_val=max_val, min_val=min_val)
        await self.session.execute(query)

    async def delete(self, param_id: UUID):
        query = delete(Parameter).where(Parameter.id==param_id)
        await self.session.execute(query)
