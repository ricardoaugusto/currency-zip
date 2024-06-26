import sys
from src.czip.currency_conversion import convert


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python czip.py <currency_string> [--when=<YYYYMMDD>]")
        sys.exit(1)

    currency_string = sys.argv[1]
    when_param = None

    if len(sys.argv) == 3:
        option = sys.argv[2]
        if option.startswith("--when="):
            when_param = option.split("=")[1]

    result = convert(currency_string, when_param)
    print(result)


if __name__ == "__main__":
    main()
