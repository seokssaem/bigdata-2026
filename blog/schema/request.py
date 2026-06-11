from pydantic import BaseModel

# 게시글 생성 요청 모델
class BlogCreateRequest(BaseModel):
    title: str
    content: str

# 게시글 수정 요청 모델
class BlogUpdateRequest(BaseModel):
    title: str | None=None
    content: str | None=None