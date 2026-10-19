from datetime import datetime

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None

class ProjectUpdate(BaseModel):
    name: str
    description: str | None = None
    
class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime

    model_config = {
        "from_attributes": True
    }