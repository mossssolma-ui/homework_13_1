from unittest.mock import patch

from _pytest.capture import CaptureFixture

from src.external_api import convert_to_rub


def test_correct_currency():
    """Неподдерживаемая валюта. Возвращает 0.0"""
    result = convert_to_rub(120, 'KZT')
    assert result == 0.0


@patch("src.external_api.requests.get", side_effect=Exception)
def test_convert_to_rub_error(mock_get, capsys: CaptureFixture):
    """Тест исключения. Возвращает сообщение и 0.0 """
    result = convert_to_rub('', 'USD')
    captured = capsys.readouterr()
    assert "Ошибка запроса:" in captured.out
    assert result == 0.0


@patch("src.external_api.requests.get")
def test_convert_to_rub_no_200(mock_get, capsys: CaptureFixture):
    """Тестируем когда статус код != 200"""
    mock_get.return_value.status_code = 400
    result = convert_to_rub('', 'USD')
    captured = capsys.readouterr()
    assert 'Ошибка запроса:' in captured.out
    assert result == 0.0


@patch("src.external_api.requests.get")
def test_convert_to_rub_success(mock_get, capsys: CaptureFixture):
    """Ключ success существует"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'success': True, 'result': 200.00}
    result = convert_to_rub(120, 'USD')
    captured = capsys.readouterr()
    assert '' == captured.out
    assert result == 200.00


@patch("src.external_api.requests.get")
def test_convert_to_rub_no_success(mock_get, capsys: CaptureFixture):
    """Ключ success не существует"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {'success': False, 'result': 200.00}
    result = convert_to_rub(120, 'USD')
    captured = capsys.readouterr()
    assert '' == captured.out
    assert result == 0.0
