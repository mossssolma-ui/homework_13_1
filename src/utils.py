import json
import logging

from .external_api import convert_to_rub

logger = logging.getLogger("utils")
file_handler = logging.FileHandler("logs/utils.log", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def load_financial_transactions(file_path: str) -> list[dict]:
    """
    Функция принимает JSON-файл в качестве аргумента
    и возвращает список словарей с данными о финансовых транзакциях.

    Если JSON-файл пустой, содержит не-список или не найден,
    возвращается пустой список.
    """
    try:
        logger.debug(f"Загрузка транзакции из файла {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            result = json.load(f)
            if isinstance(result, list):
                logger.info(f"Успешно загружено {len(result)} транзакций из файла {file_path}")
                return result
            else:
                logger.error(f"Ошибка загрузки из файла {file_path}")
                return []
    except FileNotFoundError as e:
        logger.error(f"Файл {file_path} не найден, ошибка {e}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования файла {file_path}: {e}")
        return []
    except Exception as e:
        logger.error(f"Неизвестная ошибка при загрузке файла{file_path}: {e}")
        return []


def get_transaction_amount(transaction: dict) -> float:
    """
    Функция принимает на вход транзакцию и возвращает сумму транзакции
    (amount) в рублях.
    Если транзакция была в USD или EUR, происходит вызов
    функции convert_to_rub, которая обращается к внешнему API
    """
    try:
        logger.debug("Начало обработки транзакции для получения суммы в рублях")
        operation = transaction.get("operationAmount")

        if not isinstance(operation, dict):
            logger.error("Поле 'operationAmount' не является словарем")
            return 0.0

        amount = float(operation.get("amount", 0))
        logger.debug(f"Получена сумма: {amount}")

        cur = operation.get("currency")
        if isinstance(cur, dict):
            cur_code = cur.get("code")
            logger.debug(f"Код валюты: {cur_code}")
        else:
            logger.error("Поле 'currency' не является словарем")
            return 0.0

        if cur_code == "RUB":
            logger.debug("Валюта в RUB, конвертация не нужна")
            return amount
        elif cur_code in ["USD", "EUR"]:
            logger.debug(f"Поступила валюта {cur_code}, выполняется конвертация в RUB")
            to_rub = convert_to_rub(amount, cur_code)
            if to_rub is not None:
                logger.info(f"Успешная конвертация {amount} {cur_code}: {to_rub} в RUB")
                return to_rub
            else:
                logger.error(f"Ошибка конвертации {amount} {cur_code}: {to_rub} в RUB")
                return 0.0
        else:
            logger.error(f"Данная валюта не обрабатывается {cur_code}")
            return 0.0
    except Exception as e:
        logger.error(f"Неизвестная ошибка при обработке транзакции {e}")
        return 0.0
