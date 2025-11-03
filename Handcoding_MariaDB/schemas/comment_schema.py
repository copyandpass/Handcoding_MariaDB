from pydantic import BaseModel
from datetime import datetime
from .user_schema import UserSchema # 댓글 작성자 정보를 위함

# 기본적인 Comment 데이터 형태
class CommentBase(BaseModel):
    content: str

# 댓글 생성 시 받을 데이터
class CommentCreate(CommentBase):
    pass

# API 응답으로 보낼 댓글 데이터
class CommentSchema(CommentBase):
    comment_id: int
    post_id: int
    user_id: int
    created_at: datetime
    owner: UserSchema # 작성자 정보를 담기 위한 관계 설정

    class Config:
        from_attributes = True