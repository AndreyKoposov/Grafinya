from typing import Optional, Any
from pydantic import BaseModel, Field


class ProcessData(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

class ProcessResponse(BaseModel):
    processes: dict[str, Any] = Field(...)
