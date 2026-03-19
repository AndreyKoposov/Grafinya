from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=20)
    orioks_id: Optional[str] = Field(None)

class LoginResponse(BaseModel):
    success: bool
    error: Optional[str] = None

class SessionResponse(BaseModel):
    user_id: str
    user_name: str
    logged_at: datetime
