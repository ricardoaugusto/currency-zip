from datetime import datetime

from forex_python.converter import CurrencyRates


class ExchangeRate:
    @staticmethod
    def convert_to(amount, from_currency, to_currency, when=datetime.now()):
        c = CurrencyRates()
        rate = c.get_rate(from_currency, to_currency, when)

        converted_amount = amount * rate
        return round(converted_amount, 2)
