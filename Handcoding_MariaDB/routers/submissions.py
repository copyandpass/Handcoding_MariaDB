import os
import uuid
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
import mysql.connector
from schemas.submission_schema import SubmissionCreateResponse, SubmissionResult
from database.dependencies import get_db_connection
from services import ocr_service  # ◀◀◀ 새로 만든 OCR 서비스 임포트

UPLOAD_DIRECTORY = "./uploaded_images"

router = APIRouter()


@router.post("/submissions", response_model=SubmissionCreateResponse)
async def upload_submission(
        content_id: int = Form(...),
        image: UploadFile = File(...),
        conn: mysql.connector.MySQLConnection = Depends(get_db_connection)
):
    """
    사용자가 이미지를 업로드하면 서버에 저장하고, Gemini API로 채점 후 결과를 DB에 저장합니다.
    """
    # 1. 이미지 파일 저장
    os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIRECTORY, f"{uuid.uuid4()}.jpg")
    try:
        with open(file_path, "wb") as buffer:
            content = await image.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"파일 저장 중 오류 발생: {e}")

    cursor = conn.cursor(dictionary=True)
    try:
        # 2. DB에서 정답 코드 조회
        cursor.execute("SELECT answer_code FROM CONTENT WHERE content_id = %s", (content_id,))
        content = cursor.fetchone()
        if not content:
            raise HTTPException(status_code=404, detail="해당 ID의 콘텐츠를 찾을 수 없습니다.")
        answer_code = content['answer_code']

        # 3. OCR 서비스 호출하여 채점 실행
        base64_image = ocr_service.encode_image_to_base64(file_path)
        extracted_code = ocr_service.get_text_from_image(base64_image)

        if not extracted_code:
            raise HTTPException(status_code=500, detail="Gemini API를 통한 코드 추출에 실패했습니다.")

        scoring_result = ocr_service.compare_codes(extracted_code, answer_code)

        # 4. DB에 제출 기록 생성 (채점 결과 포함)
        query = """
                INSERT INTO SUBMISSIONS
                (user_id, content_id, image_path, status, converted_code, accuracy, is_correct, score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) \
                """
        # TODO: 실제 로그인 기능 구현 후 user_id는 토큰 등에서 가져와야 함
        submission_data = (
            1, content_id, file_path, 'COMPLETED',
            scoring_result['converted_code'],
            scoring_result['accuracy'],
            scoring_result['is_correct'],
            scoring_result['score']
        )
        cursor.execute(query, submission_data)
        conn.commit()

        submission_id = cursor.lastrowid
        return {"submission_id": submission_id, "message": "Submission and scoring completed."}

    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"DB 처리 중 오류: {err}")
    finally:
        cursor.close()


@router.get("/submissions/{submission_id}", response_model=SubmissionResult)
def get_submission_result(submission_id: int, conn: mysql.connector.MySQLConnection = Depends(get_db_connection)):
    """주어진 submission_id에 해당하는 제출 결과 및 상태를 조회합니다."""
    cursor = conn.cursor(dictionary=True)
    try:
        query = "SELECT * FROM SUBMISSIONS WHERE submission_id = %s"
        cursor.execute(query, (submission_id,))
        submission = cursor.fetchone()
        if submission is None:
            raise HTTPException(status_code=404, detail="해당 제출 기록을 찾을 수 없습니다.")
        return submission
    finally:
        cursor.close()