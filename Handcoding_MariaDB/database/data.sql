-- data.sql

-- =================================================================
-- USERS Table: 초기 사용자 데이터 추가
-- =================================================================
INSERT INTO USERS (email, password, nickname) VALUES
('user1@example.com', 'hashed_password_1', '코딩천재'),
('user2@example.com', 'hashed_password_2', '알고리즘마스터');


-- =================================================================
-- CONTENT Table: 초기 문제 데이터 추가 (answer_code 포함)
-- =================================================================
-- database/data.sql (INSERT 구문 수정)

INSERT INTO CONTENT (title, description, difficulty, answer_code) VALUES
('문제 1: Hello World', '화면에 Hello World를 출력하는 코드를 작성하세요.', 'Easy', 'print("Hello World")'),
('문제 2: A+B', '두 정수 A와 B를 입력받아 합을 출력하는 프로그램을 작성하세요.', 'Easy', 'A, B = map(int, input().split())\nprint(A+B)'),
('문제 3: 팩토리얼', '주어진 수 N의 팩토리얼(N!)을 구하는 프로그램을 작성하세요.', 'Normal', 'def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)\n\nN = int(input())\nprint(factorial(N))');


-- =================================================================
-- SUBMISSIONS Table: 초기 제출 기록 데이터 추가 (content_id 사용)
-- =================================================================
INSERT INTO SUBMISSIONS (user_id, content_id, image_path, converted_code, success_rate, status) VALUES
(1, 1, '/images/submission_1.jpg', 'print("Hello World")', 0.99, 'COMPLETED'),
(2, 1, '/images/submission_2.jpg', 'console.log("Hello World")', 0.95, 'COMPLETED'),
(1, 2, '/images/submission_3.jpg', 'A, B = map(int, input().split())\nprint(A+B)', 1.0, 'COMPLETED');

-- =================================================================
-- POSTS Table: 초기 게시글 데이터 추가
-- =================================================================
INSERT INTO POSTS (user_id, title, content) VALUES
(1, 'FastAPI 질문 있습니다!', 'FastAPI에서 백그라운드 작업을 구현하려면 어떻게 해야 하나요?'),
(2, '손코딩 팁 공유합니다', '코딩할 때 손으로 먼저 구조를 그려보면 정말 도움이 많이 됩니다.');

-- =================================================================
-- COMMENTS Table: 초기 댓글 데이터 추가
-- =================================================================
-- post_id 1번 글에 대한 댓글
INSERT INTO COMMENTS (post_id, user_id, content) VALUES
(1, 2, 'Celery 같은 라이브러리를 사용하면 쉽게 구현할 수 있어요!'),
-- post_id 2번 글에 대한 댓글
(2, 1, '좋은 팁 감사합니다!');

-- =================================================================
-- ANNOUNCEMENTS Table: 초기 공지사항 데이터 추가
-- =================================================================
-- admin_id는 관리자 권한을 가진 user_id를 의미합니다. (여기서는 1번 유저를 관리자로 가정)
INSERT INTO ANNOUNCEMENTS (admin_id, title, content) VALUES
(1, '손코딩 서비스 정식 오픈 안내', '안녕하세요! 손코딩 이미지 변환 서비스가 정식 오픈했습니다. 많은 이용 부탁드립니다.');