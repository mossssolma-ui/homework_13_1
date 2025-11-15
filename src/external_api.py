import os

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(amount: float, currency: str) -> float:
    """Функция конвертации валюты через API

    :param amount: принимает сумму в валюте USD или EUR
    :param currency: принимает валюту в которую нужно перевести
    :return: возвращает конвертированную сумму в RUB
    """
    if currency not in ["USD", "EUR"]:
        return 0.0

    params = {"to": "RUB", "from": currency, "amount": amount}

    headers = {"apikey": API_KEY}

    try:
        response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)  # type: ignore
        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                return float(data["result"])
            else:
                return 0.0
        else:
            print(f"Ошибка запроса: {response.status_code}")
            return 0.0
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return 0.0
