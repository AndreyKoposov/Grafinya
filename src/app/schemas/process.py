from pydantic import BaseModel, Field


class ProcessCreateData(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)

class ProcessEditData(BaseModel):
    pr_id: str = Field(...)
    new_name: str = Field("", min_length=3, max_length=50)

class EntityData(BaseModel):
    proc_id: str = Field(...)
    entity_id: str = Field(...)
    name: str = Field("", min_length=3, max_length=50)
    tag: str = Field("", min_length=3, max_length=50)

class ToDeleteData(BaseModel):
    id: str = Field(...)
