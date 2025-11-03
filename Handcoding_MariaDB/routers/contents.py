from fastapi import APIRouter, HTTPException, Depends
import mysql.connector
from schemas.content_schema import Content
from database.dependencies import get_db_connection  # 중앙 관리 함수 임포트

router = APIRouter()


@router.get("/contents", response_model=list[Content])
def get_contents_list(conn: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    """DB에 저장된 모든 콘텐츠 목록을 조회합니다."""
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT content_id, title, description, difficulty, answer_code FROM CONTENT")
        contents = cursor.fetchall()
        return contents
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        raise HTTPException(status_code=500, detail="데이터베이스 처리 중 오류가 발생했습니다.")
    finally:
        cursor.close()


@router.get("/content/{content_id}", response_model=Content)
def get_content_by_id(content_id: int, conn: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    """주어진 content_id에 해당하는 특정 문제의 상세 정보를 조회합니다."""
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT content_id, title, description, difficulty, answer_code FROM CONTENT WHERE content_id = %s"
        cursor.execute(query, (content_id,))
        content = cursor.fetchone()

        if content is None:
            raise HTTPException(status_code=404, detail="해당 ID의 문제를 찾을 수 없습니다.")

        return content
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        raise HTTPException(status_code=500, detail="데이터베이스 처리 중 오류가 발생했습니다.")
    finally:
        cursor.close()