from pydantic import BaseModel

class BlogResponse(BaseModel):
    id: int
    title: str
    content: str