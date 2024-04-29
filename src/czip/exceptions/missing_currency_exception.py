class MissingCurrencyException(Exception):
    def __init__(self):
        super().__init__("Missing Currency to convert to.")
