from pydantic import BaseModel

# 게시글 생성
class BlogCreateRequest(BaseModel):
    title: str
    content: str

# 게시글 수정
class BlogUpdateRequest(BaseModel):
    title: str | None = None
    content: str | None = None