from unittest.mock import patch

import pandas as pd

from src.csv_excel import get_convert_csv_to_list_dict, get_convert_excel_to_list_dict


@patch("src.csv_excel.pd.read_csv")
def test_get_convert_csv_to_list_dict(mock_read_csv):
    mock_read_csv.return_value = pd.DataFrame(
        {"id": [650703, 3598919], "amount": [16210, 29740], "description": ["Счет", "Discover"]}
    )
    result = get_convert_csv_to_list_dict("file.csv")
    assert result == [
        {"id": 650703, "amount": 16210, "description": "Счет"},
        {"id": 3598919, "amount": 29740, "description": "Discover"},
    ]


@patch("src.csv_excel.pd.read_csv", side_effect=FileNotFoundError)
def test_get_convert_csv_to_list_dict_no_file(mock_read_csv):
    """Файл не найден, возвращает []"""
    result = get_convert_csv_to_list_dict("trans.csv")
    assert result == []


@patch("src.csv_excel.pd.read_csv", side_effect=Exception)
def test_get_convert_csv_to_list_dict_exception(mock_read_csv):
    """Неизвестная ошибка, возвращает []"""
    result = get_convert_csv_to_list_dict("trans.csv")
    assert result == []


# тест функции get_convert_excel_to_list_dict
@patch("src.csv_excel.pd.read_excel")
def test_get_convert_excel_to_list_dict(mock_read_excel):
    mock_read_excel.return_value = pd.DataFrame(
        {"id": [650703, 3598919], "amount": [16210, 29740], "description": ["Счет", "Discover"]}
    )
    result = get_convert_excel_to_list_dict("file.xlsx")
    assert result == [
        {"id": 650703, "amount": 16210, "description": "Счет"},
        {"id": 3598919, "amount": 29740, "description": "Discover"},
    ]


@patch("src.csv_excel.pd.read_excel", side_effect=FileNotFoundError)
def test_get_convert_excel_to_list_dict_no_file(mock_read_excel):
    """Файл не найден, возвращает []"""
    result = get_convert_excel_to_list_dict("trans.xlsx")
    assert result == []


@patch("src.csv_excel.pd.read_excel", side_effect=Exception)
def test_get_convert_excel_to_list_dict_exception(mock_read_excel):
    """Неизвестная ошибка, возвращает []"""
    result = get_convert_excel_to_list_dict("trans.xlsx")
    assert result == []
