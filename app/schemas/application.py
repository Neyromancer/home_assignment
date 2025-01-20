from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    description: str


class ApplicationResponse(ApplicationBase):
    id: int
    created_at: datetime