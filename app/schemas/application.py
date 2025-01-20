from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApplicationBase(BaseModel):
    user_name: str
    description: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ApplicationResponse(ApplicationBase):
    id: int
