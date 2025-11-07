from src.masks import get_mask_account, get_mask_card_number
from src.utils import get_transaction_amount, load_financial_transactions


def main() -> None:
    # вызов функции из masks
    card_mask = get_mask_card_number(1234567890123456)
    account_mask = get_mask_account(1234567890)

    print("Маска карты:", card_mask)
    print("Маска счёта:", account_mask)

    # Вызов функции из utils
    transactions = load_financial_transactions("data/operations.json")
    if transactions:
        amount = get_transaction_amount(transactions[0])
        print("Сумма транзакции в рублях:", amount)


if __name__ == "__main__":
    main()
