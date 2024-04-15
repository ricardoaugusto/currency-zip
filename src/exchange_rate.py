from forex_python.converter import CurrencyRates, RatesNotAvailableError


def convert_to(amount, from_currency, to_currency, when):
    try:
        c = CurrencyRates()
        rate = c.get_rate(from_currency, to_currency, when)

        converted_amount = amount * rate
        return round(converted_amount, 2)
    except RatesNotAvailableError:
        # Generic error when the currency is unknown or not supported
        print("Rates are not available.")
        return 0.0
