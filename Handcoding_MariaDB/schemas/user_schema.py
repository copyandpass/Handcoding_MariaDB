from pydantic import BaseModel, EmailStr

# 공통적으로 사용될 기본 스키마
class UserBase(BaseModel):
    email: EmailStr
    nickname: str | None = None

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    user_id: int

    class Config:
        from_attributes = True