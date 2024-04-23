import sys
from src.currency_conversion import run_exchange


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python czip.py <currency_string> [--when=<YYYYMMDD>]")
        sys.exit(1)

    currency_string = sys.argv[1]
    when_param = None

    if len(sys.argv) == 3:
        option = sys.argv[2]
        if option.startswith("--when="):
            when_param = option.split("=")[1]

    result = run_exchange(currency_string, when_param)
    print(result)
