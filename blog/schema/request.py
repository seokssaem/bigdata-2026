from pydantic import BaseModel
from typing import Optional

class BlogCreateRequest(BaseModel):
    title: str
    content: str

class BlogUpdateRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None