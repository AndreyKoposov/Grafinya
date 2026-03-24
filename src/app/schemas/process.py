from pydantic import BaseModel, Field


class ProcessCreateData(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

class ProcessEditData(BaseModel):
    pr_id: str = Field(...)
    new_name: str = Field("", min_length=3, max_length=50)
