import logging

logger = logging.getLogger("masks")
file_handler = logging.FileHandler("logs/masks.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s: %(name)s: %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: int) -> str:
    """
    Функция маскировки банковской карты.
    Принимает на вход номер карты и возвращает ее маску
    """
    try:
        logger.debug(f"Начало маскировки номера карты: {card_number}")
        my_card_number = str(card_number)
        if len(my_card_number) >= 16:
            card_text = my_card_number[:6] + "*" * (len(my_card_number) - 10) + my_card_number[-4:]
            result = " ".join([card_text[i : i + 4] for i in range(0, len(card_text), 4)])
            logger.info(f"Маскировка номера карты успешно завершена {result}")
        else:
            result = my_card_number
            logger.error(f"Ошибка, номер карты меньше 16 символов: {result}, маскировка не выполнена.")
        return result
    except Exception as e:
        logger.error(f"Ошибка при маскировке номера карты {card_number}: {e}")
        raise


def get_mask_account(account_number: int) -> str:
    """
    Функция маскировки банковского счета.
    Принимает на вход номер счета и возвращает его маску.
    """
    try:
        logger.debug(f"Начало маскировки номера счета: {account_number}")
        if not isinstance(account_number, int):
            text_error = "Номер счета должен быть целым числом"
            logger.error(text_error)
            raise TypeError(text_error)
        account_number_str = str(account_number)
        if len(account_number_str) >= 5:
            result = "**" + account_number_str[-4:]
            logger.info(f"Маскировка счета успешно завершена {result}")
        else:
            result = account_number_str
            logger.error(f"Ошибка, номер счета меньше 5 символов: {result}, маскировка не выполнена.")
        return result
    except Exception as e:
        logger.error(f"Ошибка при маскировке счета: {account_number}: {e}")
        raise
