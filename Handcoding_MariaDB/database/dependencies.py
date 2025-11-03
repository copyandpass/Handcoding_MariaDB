import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}

def get_db_connection():
    """FastAPI의 의존성 주입을 통해 DB 커넥션을 제공하는 함수"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn  # API 함수에 연결(conn)을 전달
    finally:
        # API 함수가 끝나면 연결을 자동으로 닫음
        if 'conn' in locals() and conn.is_connected():
            conn.close()