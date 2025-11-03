from fastapi import APIRouter, HTTPException, Depends
import mysql.connector
from schemas import announcement_schema
from database.dependencies import get_db_connection # ◀◀◀ 중앙 관리 함수 임포트

router = APIRouter(
    prefix="/announcements",
    tags=["Announcements"]
)

# 삭된 부분: 이 파일 안에 있던 get_db_connection 함수를 삭제합니다.

@router.get("/", response_model=list[announcement_schema.AnnouncementSchema])
def get_announcements_list(conn: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    """전체 공지사항 목록을 조회합니다."""
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM ANNOUNCEMENTS ORDER BY created_at DESC")
        announcements = cursor.fetchall()
        return announcements
    finally:
        cursor.close()

# TODO: 공지사항 생성, 수정, 삭제 API는 관리자 권한을 확인하는 로직을 추가해야 합니다.