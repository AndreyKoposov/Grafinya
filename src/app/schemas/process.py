from typing import Optional
from pydantic import BaseModel, Field


class ProcessData(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
