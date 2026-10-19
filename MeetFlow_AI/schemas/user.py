# ==================================================================
# C:\Users\Administrator\meetflow_ai\schemas\user.py
# User CRUD를 만들어서 실제 사용자 데이터를 PostgreSQL에 저장
# ==================================================================

from pydantic import BaseModel, EmailStr


# 사용자가 입력할 데이터
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# API가 사용자에게 보여줄 데이터
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    profile_image: str | None = None

    model_config = {"from_attributes": True}

