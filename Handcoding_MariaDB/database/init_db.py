# database/init_db.py

import os
from dotenv import load_dotenv
import mysql.connector

# .env 파일에서 환경 변수 로드
load_dotenv()

# DB 접속 정보 가져오기
DB_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_NAME")
}


def execute_sql_file(file_path):
    """주어진 경로의 .sql 파일을 읽어 실행하는 함수"""
    try:
        # DB에 먼저 연결
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        with open(file_path, 'r', encoding='utf-8') as f:
            # .sql 파일의 각 명령어(; 기준)를 분리하여 실행
            sql_commands = f.read().split(';')
            for command in sql_commands:
                if command.strip():
                    cursor.execute(command)

        conn.commit()
        print(f"✅ Successfully executed {os.path.basename(file_path)}")

    except mysql.connector.Error as err:
        print(f"❌ Error executing {os.path.basename(file_path)}: {err}")

    finally:
        # 연결 종료
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()


def initialize_database():
    """데이터베이스 초기화를 총괄하는 함수"""
    print("🚀 Starting database initialization...")
    # 1. 테이블 구조 생성
    execute_sql_file('database/schema.sql')
    # 2. 초기 데이터 삽입
    execute_sql_file('database/data.sql')
    print("✨ Database initialization finished.")