from pydantic import BaseModel

class ContentBase(BaseModel):
    title: str
    description: str | None = None
    difficulty: str | None = None
    answer_code: str | None = None # <<-- 정답 코드 필드 추가!

class Content(ContentBase):
    content_id: int

    class Config:
        from_attributes = True