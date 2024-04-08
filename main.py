from src.currency_parser import CurrencyParser


if __name__ == "__main__":
    currency_string = "100EUR + 350USD + 10000BRL to EUR"

    parser = CurrencyParser()
    result = parser.run_exchange(currency_string)
    print(result)
