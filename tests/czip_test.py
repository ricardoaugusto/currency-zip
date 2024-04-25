import sys
from io import StringIO
from unittest.mock import patch
import pytest
import czip


@patch("czip.convert")
def test_main(mock_convert):
    mock_convert.return_value = "10.00 USD"

    mocked_stdout = StringIO()
    with patch.object(sys, "stdout", mocked_stdout):
        with patch.object(sys, "argv", ["czip.py", "USD"]):
            czip.main()

    mock_convert.assert_called_once_with("USD", None)
    assert mocked_stdout.getvalue().strip() == "10.00 USD"


@patch("czip.convert")
def test_main_with_when_param(mock_convert):
    mock_convert.return_value = "10.00 USD"

    mocked_stdout = StringIO()
    with patch.object(sys, "stdout", mocked_stdout):
        with patch.object(sys, "argv", ["czip.py", "USD", "--when=20220425"]):
            czip.main()

    mock_convert.assert_called_once_with("USD", "20220425")
    assert mocked_stdout.getvalue().strip() == "10.00 USD"


def test_main_without_currency():
    with patch.object(sys, "argv", ["czip.py", None]):
        with patch("sys.exit"):
            with pytest.raises(Exception):
                czip.main()


def test_main_with_invalid_argument_count():
    with patch.object(sys, "argv", ["czip.py", "USD", "unknown_extra_arg"]):
        with patch("sys.exit"):
            with pytest.raises(Exception):
                czip.main()


def test_main_with_invalid_argument_count_when_param():
    with patch.object(
        sys, "argv", ["czip.py", "USD", "--when=20220425", "unknown_extra_arg"]
    ):
        with patch("sys.exit"):
            with pytest.raises(Exception):
                czip.main()


def test_main_entry_point():
    with patch.object(sys, "argv", ["czip.py", "USD"]):
        with patch("czip.main") as mock_main:
            czip.__name__ = "__main__"
            czip.main()
            mock_main.assert_called_once()
