import os
import base64
import requests
import Levenshtein
import json
import re
from dotenv import load_dotenv

load_dotenv()

# .env 파일에서 Gemini API 키를 불러옵니다.
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={API_KEY}"


def encode_image_to_base64(image_path: str):
    """이미지 파일을 Base64 문자열로 인코딩합니다."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

#
def get_text_from_image(base64_image: str):
    """Gemini API를 호출하여 이미지에서 텍스트를 추출합니다."""
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [{
            "parts": [
                {"text": "이미지에서 손글씨로 작성된 코드만 텍스트로 추출해줘. 줄 번호가 매겨진 코드 블록의 텍스트만 추출하고, 줄바꿈을 유지해줘."},
                {"inlineData": {"mimeType": "image/jpeg", "data": base64_image}}
            ]
        }]
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        result = response.json()
        extracted_text = result['candidates'][0]['content']['parts'][0]['text']

        match = re.search(r'```(?:python|)\n(.*?)```', extracted_text, re.DOTALL)
        return match.group(1).strip() if match else extracted_text.strip()
    except Exception:
        return None


def compare_codes(extracted_code: str, answer_code: str):
    """추출된 코드와 정답 코드를 비교하여 채점 결과를 반환합니다."""
    extracted_lines = [line.strip() for line in extracted_code.split('\n') if line.strip()]
    answer_lines = [line.strip() for line in answer_code.split('\n') if line.strip()]

    total_chars = sum(max(len(e), len(a)) for e, a in zip(extracted_lines, answer_lines))
    total_distance = sum(Levenshtein.distance(e, a) for e, a in zip(extracted_lines, answer_lines))

    accuracy = (1 - total_distance / total_chars) * 100 if total_chars > 0 else 0
    is_correct = accuracy == 100.0 and len(extracted_lines) == len(answer_lines)
    score = 100 if is_correct else int(accuracy)

    return {
        "converted_code": extracted_code,
        "accuracy": round(accuracy, 2),
        "is_correct": is_correct,
        "score": score
    }