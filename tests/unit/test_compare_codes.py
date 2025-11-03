from Handcoding_MariaDB.services.ocr_service import compare_codes


def test_compare_codes_exact_match():
    extracted = "print('hello')\n"
    answer = "print('hello')\n"

    result = compare_codes(extracted, answer)

    assert result['is_correct'] is True
    assert result['score'] == 100
    assert float(result['accuracy']) == 100.0


def test_compare_codes_partial_mismatch():
    extracted = "print('hello')\n"
    answer = "print('world')\n"

    result = compare_codes(extracted, answer)

    assert result['is_correct'] is False
    assert 0 <= result['accuracy'] <= 100
