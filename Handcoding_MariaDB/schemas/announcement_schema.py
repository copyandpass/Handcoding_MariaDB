from pydantic import BaseModel
from datetime import datetime

# 기본적인 Announcement 데이터 형태
class AnnouncementBase(BaseModel):
    title: str
    content: str | None = None

# 공지사항 생성 시 받을 데이터
class AnnouncementCreate(AnnouncementBase):
    pass

# API 응답으로 보낼 공지사항 데이터
class AnnouncementSchema(AnnouncementBase):
    announcement_id: int
    admin_id: int
    created_at: datetime

    class Config:
        from_attributes = True