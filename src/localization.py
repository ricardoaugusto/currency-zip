import locale


def delocalize_currency(amount_str, currency):
    """
    Remove any localized punctuation from the amount_str

    :param amount_str:
    :param currency:
    :return:
    """
    currency_locale_map = {
        "USD": "en_US.UTF-8",
        "EUR": "pt_PT.UTF-8",
        "BRL": "pt_BR.UTF-8",
        "GBP": "en_GB.UTF-8",
    }

    locale_setting = currency_locale_map.get(currency, "en_US.UTF-8")
    locale.setlocale(locale.LC_NUMERIC, locale_setting)

    amount = locale.atof(amount_str)
    return amount
