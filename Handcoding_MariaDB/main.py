# main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from routers.contents import router as content_router
from routers.submissions import router as submissions_router
from database.init_db import initialize_database
from routers.community import router as community_router
from routers.announcements import router as announcements_router

# FastAPI 시작/종료 시 실행될 로직을 관리합니다.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 실행될 코드
    print("Server is starting up...")
    initialize_database()
    yield
    # 서버 종료 시 실행될 코드
    print("Server is shutting down...")

# app 생성 시 lifespan 이벤트를 등록합니다.
app = FastAPI(lifespan=lifespan)

# 라우터들을 연결합니다.
app.include_router(content_router, prefix="/api", tags=["Content"])
app.include_router(submissions_router, prefix="/api", tags=["Submissions"])
app.include_router(community_router, prefix="/api", tags=["Community"]) # 커뮤니티 라우터 추가
app.include_router(announcements_router, prefix="/api", tags=["Announcements"]) # 공지사항 라우터 추가


@app.get("/")
def read_root():
    return {"message": "손코딩 API 서버에 오신 것을 환영합니다!"}