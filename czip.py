import sys

from src.currency_parser import run_exchange

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python czip.py <currency_string>")
        sys.exit(1)

    currency_string = sys.argv[1]

    result = run_exchange(currency_string)
    print(result)
