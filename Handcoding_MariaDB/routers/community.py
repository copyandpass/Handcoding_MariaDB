from fastapi import APIRouter, HTTPException, Depends
import mysql.connector
from schemas import post_schema, comment_schema, user_schema
from database.dependencies import get_db_connection # ◀◀◀ DB 연결은 이 한 줄로 통일합니다.

router = APIRouter(
    prefix="/community",
    tags=["Community"]
)

# --- 게시글(Posts) API ---

@router.post("/posts", response_model=post_schema.PostSchema, status_code=201)
def create_post(post: post_schema.PostCreate, conn: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    """새로운 게시글을 생성합니다."""
    # TODO: 실제 로그인 기능 구현 후 user_id는 토큰 등에서 가져와야 함 (지금은 1로 고정)
    user_id = 1
    cursor = conn.cursor(dictionary=True)
    try:
        query = "INSERT INTO POSTS (title, content, user_id) VALUES (%s, %s, %s)"
        cursor.execute(query, (post.title, post.content, user_id))
        conn.commit()
        post_id = cursor.lastrowid

        # 방금 생성된 게시글 정보를 다시 조회하여 반환 (JOIN 사용)
        cursor.execute("""
                       SELECT p.*, u.user_id, u.email, u.nickname
                       FROM POSTS p
                       JOIN USERS u ON p.user_id = u.user_id
                       WHERE p.post_id = %s
                       """, (post_id,))
        new_post_data = cursor.fetchone()

        owner_data = {
            "user_id": new_post_data['user_id'],
            "email": new_post_data['email'],
            "nickname": new_post_data['nickname']
        }
        new_post_data['owner'] = user_schema.UserSchema(**owner_data)
        return new_post_data
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"DB 오류: {err}")
    finally:
        cursor.close()


@router.get("/posts", response_model=list[post_schema.PostSchema])
def get_posts_list(conn: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    """전체 게시글 목록을 조회합니다."""
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
                       SELECT p.*, u.user_id, u.email, u.nickname
                       FROM POSTS p
                       JOIN USERS u ON p.user_id = u.user_id
                       ORDER BY p.created_at DESC
                       """)
        posts_data = cursor.fetchall()

        result = []
        for post in posts_data:
            owner_data = {
                "user_id": post['user_id'],
                "email": post['email'],
                "nickname": post['nickname']
            }
            post['owner'] = user_schema.UserSchema(**owner_data)
            result.append(post)
        return result
    finally:
        cursor.close()


# --- 댓글(Comments) API ---

@router.post("/posts/{post_id}/comments", response_model=comment_schema.CommentSchema, status_code=201)
def create_comment_for_post(post_id: int, comment: comment_schema.CommentCreate,
                            conn: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    """특정 게시글에 새로운 댓글을 생성합니다."""
    # TODO: 실제 로그인 기능 구현 후 user_id는 토큰 등에서 가져와야 함 (지금은 2로 고정)
    user_id = 2
    cursor = conn.cursor(dictionary=True)
    try:
        query = "INSERT INTO COMMENTS (post_id, user_id, content) VALUES (%s, %s, %s)"
        cursor.execute(query, (post_id, user_id, comment.content))
        conn.commit()
        comment_id = cursor.lastrowid

        cursor.execute("""
                       SELECT c.*, u.user_id, u.email, u.nickname
                       FROM COMMENTS c
                       JOIN USERS u ON c.user_id = u.user_id
                       WHERE c.comment_id = %s
                       """, (comment_id,))
        new_comment_data = cursor.fetchone()

        owner_data = {
            "user_id": new_comment_data['user_id'],
            "email": new_comment_data['email'],
            "nickname": new_comment_data['nickname']
        }
        new_comment_data['owner'] = user_schema.UserSchema(**owner_data)
        return new_comment_data
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"DB 오류: {err}")
    finally:
        cursor.close()