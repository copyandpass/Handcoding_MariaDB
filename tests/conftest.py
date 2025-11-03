import sys
import types
import os
import pytest

# Ensure Python can import the project's package/routers when tests import `Handcoding_MariaDB`.
# Insert the inner package folder (Handcoding_MariaDB/Handcoding_MariaDB) into sys.path.
_tests_dir = os.path.dirname(__file__)
_repo_root = os.path.dirname(_tests_dir)
_inner_pkg = os.path.join(_repo_root, "Handcoding_MariaDB")
if _inner_pkg not in sys.path:
    sys.path.insert(0, _inner_pkg)

# Provide a top-level shim for `Levenshtein` so collection doesn't attempt to load the
# C-extension. This must run at import time (before tests are collected).
if 'Levenshtein' not in sys.modules:
    def _py_distance(a: str, b: str) -> int:
        # simple, deterministic distance used only for tests (not full Levenshtein)
        if a == b:
            return 0
        # count differing positions and length difference
        diff = sum(1 for x, y in zip(a, b) if x != y)
        diff += abs(len(a) - len(b))
        return diff

    sys.modules['Levenshtein'] = types.SimpleNamespace(distance=_py_distance)


@pytest.fixture(autouse=True)
def test_shims(monkeypatch):
    """테스트 환경에서 외부 의존성을 안전하게 대체합니다:
    - Levenshtein C-extension이 없어도 동작하도록 shim 제공
    - 외부 네트워크 호출(requests.post)을 가로채서 더미 응답 반환
    - DB 초기화 함수들을 noop으로 치환하여 테스트 중 DB 접속을 방지
    """
    # Shim for Levenshtein
    sys.modules['Levenshtein'] = types.SimpleNamespace(distance=lambda a, b: 0)

    # Dummy response for requests.post used by OCR service
    class DummyResponse:
        def __init__(self, json_data=None):
            self._json = json_data or {}

        def raise_for_status(self):
            return None

        def json(self):
            return self._json

    def dummy_post(*args, **kwargs):
        # Return a structure similar to what get_text_from_image expects
        return DummyResponse({
            "candidates": [
                {"content": {"parts": [{"text": "```\nprint('hello')\n```"}]}}
            ]
        })

    monkeypatch.setattr("requests.post", dummy_post)

    # Prevent database initialization / SQL execution during tests
    try:
        import Handcoding_MariaDB.database.init_db as init_db
    except Exception:
        # Some import layouts may differ; try alternate import path
        try:
            import database.init_db as init_db
        except Exception:
            init_db = None

    if init_db is not None:
        monkeypatch.setattr(init_db, "execute_sql_file", lambda *a, **k: None)
        monkeypatch.setattr(init_db, "initialize_database", lambda *a, **k: None)

    yield
