from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    username: str | None = None
    description: str | None = None


class ApplicationCreate(ApplicationBase):
    pass

class ApplicationResponse(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime