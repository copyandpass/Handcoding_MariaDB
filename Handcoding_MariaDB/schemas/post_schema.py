from pydantic import BaseModel
from datetime import datetime
from .user_schema import UserSchema # User 스키마를 가져와서 작성자 정보 표시에 사용

# 기본적인 Post 데이터 형태
class PostBase(BaseModel):
    title: str
    content: str | None = None

# 게시글 생성 시 받을 데이터
class PostCreate(PostBase):
    pass

# API 응답으로 보낼 게시글 데이터 (DB에서 읽어온 정보 포함)
class PostSchema(PostBase):
    post_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    owner: UserSchema # 작성자 정보를 담기 위한 관계 설정

    class Config:
        from_attributes = True