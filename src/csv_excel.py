from typing import Any

import pandas as pd  # type: ignore


def get_convert_csv_to_list_dict(file_csv: str) -> list[dict[Any, Any]]:
    """
    Функция конвертирует файл csv в список словарей
    """
    try:
        csv_df = pd.read_csv(file_csv, sep=";", encoding="utf-8")
        transactions: list[dict[Any, Any]] = csv_df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        return []
    except Exception:
        return []


def get_convert_excel_to_list_dict(file_excel: str) -> list[dict[Any, Any]]:
    """
    Функция конвертирует файл excel в список словарей
    """
    try:
        excel_df = pd.read_excel(file_excel)
        transactions: list[dict[Any, Any]] = excel_df.to_dict(orient="records")
        return transactions
    except FileNotFoundError:
        return []
    except Exception:
        return []
