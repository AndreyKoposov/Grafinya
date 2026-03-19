from uuid import uuid4
from abc import ABC
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()

class BaseModel(base):
    id = Column(UUID, primary_key=True, default=uuid4)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f"<{self.__tablename__} #{self.id}>"
