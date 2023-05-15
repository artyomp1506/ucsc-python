import unittest
from converter.converter import Converter


class ConverterTestCase(unittest.TestCase):
    def test_convert_correct_valid_data(self):
        converter = Converter()
        result = converter.convert(from_value=3, to_value=9, amount=2)
        self.assertEqual(result, 6)

    def test_fail_when_from_value_is_zero(self):
        converter = Converter()
        from_value = 0
        to_value = 3
        amount = 2
        self.assertRaises(ValueError, converter.convert, from_value, to_value, amount)
if __name__ == "__main__":
    unittest.main("test_converter")
