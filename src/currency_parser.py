import re

from src.exceptions.missing_currency_exception import MissingCurrencyException
from src.exchange_rate import convert_to


def split_currency_amount_code(currency_string):
    match = re.match(r"(\d+)(\D+)", currency_string)
    if match:
        return int(match.group(1)), match.group(2)
    else:
        raise ValueError("Invalid currency string")


def parse_currency_string(currency_string):
    currency_list = [
        (int(amount), code)
        for amount, code in (
            split_currency_amount_code(part.strip())
            for part in currency_string.split("+")
        )
    ]
    return currency_list


def run_exchange(currency_string):
    split_currency_string = currency_string.split(" to ")
    if len(split_currency_string) != 2:
        raise MissingCurrencyException()

    result = 0
    to_currency = split_currency_string[1]
    currencies = parse_currency_string(split_currency_string[0])
    if currencies:
        for amount, from_currency in currencies:
            result += convert_to(amount, from_currency, to_currency)

    return result
