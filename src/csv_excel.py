import pandas as pd


def get_convert_csv_to_list_dict(file_csv: str) -> list[dict]:
    """
    Функция конвертирует файл csv в список словарей
    """
    try:
        csv_df = pd.read_csv(file_csv, sep=";", encoding="utf-8")
        transactions = csv_df.to_dict(orient='records')
        return transactions
    except FileNotFoundError as e:
        return []
    except Exception as e:
        return []


def get_convert_excel_to_list_dict(file_excel: str) -> list[dict]:
    """
    Функция конвертирует файл excel в список словарей
    """
    try:
        excel_df = pd.read_excel(file_excel)
        transactions = excel_df.to_dict(orient="records")
        return transactions
    except FileNotFoundError as e:
        return []
    except Exception as e:
        return []
