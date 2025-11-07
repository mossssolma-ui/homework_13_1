import json
from unittest.mock import mock_open, patch

from _pytest.capture import CaptureFixture

from src.utils import get_transaction_amount, load_financial_transactions


# тесты для функции load_financial_transactions
def test_load_valid_json():
    """Успешная загрузка списка"""
    data = [{"id": 1}, {"id": 2}]
    json_str = json.dumps(data)

    with patch("builtins.open", mock_open(read_data=json_str)) as f:
        result = load_financial_transactions("operations.json")
        f.assert_called_once_with("operations.json", "r", encoding="utf-8")
        assert result == data


def test_load_no_valid_json():
    """Некорректный JSON. Возвращает [] """
    json_str = json.dumps({"data": []})

    with patch("builtins.open", mock_open(read_data=json_str)) as f:
        result = load_financial_transactions("operations.json")
        assert result == []


@patch("builtins.open", side_effect=FileNotFoundError)
def test_file_not_found(mock_open, capsys: CaptureFixture):
    """Файл не найден, возвращает сообщение и []"""
    result = load_financial_transactions("operations.json")
    captured = capsys.readouterr()
    assert "Файл не найден" in captured.out
    assert result == []


@patch("builtins.open", side_effect=json.JSONDecodeError('555', '777', 999))
def test_json_decode_error(mock_open, capsys: CaptureFixture):
    """Некорректный JSON, возвращает сообщение и []"""
    result = load_financial_transactions("operations.json")
    captured = capsys.readouterr()
    assert "Ошибка чтения файла" in captured.out
    assert result == []


@patch("builtins.open", side_effect=Exception)
def test_empty_file(mock_open, capsys: CaptureFixture):
    """Файл пустой, возвращает сообщение и []"""
    result = load_financial_transactions("operations.json")
    captured = capsys.readouterr()
    assert "Неизвестная ошибка" in captured.out
    assert result == []


# тесты для функции get_transaction_amount
def test_mis_amount():
    """Нет ключа operationAmount возвращает 0.0"""
    data = {}
    assert get_transaction_amount(data) == 0.0


def test_operationAmount_no_dict():
    """Значение operationAmount не словрь возвращает 0.0"""
    data = {"operationAmount": "text"}
    assert get_transaction_amount(data) == 0.0


def test_currency_key_missing():
    """Отсутствие currency в operationAmount. возвращает 0.0"""
    data = {
        "operationAmount": {
            "amount": "100.00"
        }
    }
    assert get_transaction_amount(data) == 0.0


def test_cur_no_dict():
    """Значение currency не словарь, возвращает 0.0"""
    data = {
        "currency": 'text'
    }
    assert get_transaction_amount(data) == 0.0


def test_trans_to_rub():
    """Транзакция в руб, возвращает как есть"""
    data = {
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        }
    }
    assert get_transaction_amount(data) == 31957.58


@patch("src.utils.convert_to_rub", return_value=8000.00)
def test_trans_usd_to_rub(mock_convert):
    """Проверка перевода из usd в rub"""
    transactions = {
        "operationAmount": {
            "amount": "80.00",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        }
    }
    result = get_transaction_amount(transactions)
    mock_convert.assert_called_once_with(80.00, 'USD')
    assert result == 8000.00


@patch("src.utils.convert_to_rub", return_value=9274.00)
def test_trans_eur_to_rub(mock_convert):
    """Проверка перевода из eur в rub"""
    transactions = {
        "operationAmount": {
            "amount": "92.74",
            "currency": {
                "name": "EUR",
                "code": "EUR"
            }
        }
    }
    result = get_transaction_amount(transactions)
    mock_convert.assert_called_once_with(92.74, 'EUR')
    assert result == 9274.00


def test_trans_no_rub_usd_eur():
    """Транзакция других валютах. Возвращает 0.0"""
    data = {
        "operationAmount": {
            "amount": "31957.58",
            "currency": {
                "name": "тенге.",
                "code": "KZT"
            }
        }
    }
    assert get_transaction_amount(data) == 0.0
