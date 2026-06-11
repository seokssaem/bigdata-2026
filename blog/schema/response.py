from pydantic import BaseModel

# 게시글 응답 모델
class BlogResponse(BaseModel):
    id: int
    title: str
    content: str