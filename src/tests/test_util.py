import unittest
from util import to_int

class TestUtil(unittest.TestCase):
    def test_to_int_valid_numeric_string(self):
        assert to_int("123") == 123

    def test_to_int_valid_numeric_string_zero(self):
        assert to_int("0") == 0

    def test_to_int_empty_string(self):
        assert to_int("") is None

    def test_to_int_none_input(self):
        assert to_int(None) is None