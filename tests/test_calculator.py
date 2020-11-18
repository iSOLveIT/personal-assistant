import unittest
from application.app_commands import BasicCalculator    # type: ignore


class BasicCalculatorTestCase(unittest.TestCase):
    def test_basic_arithmetic_in_numbers(self) -> None:
        testcase: str = "24345 plus 2"
        expected: int = 24347
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_basic_arithmetic_in_words(self) -> None:
        testcase: str = "two thousand and twenty / two"
        expected: int = 1010
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_negative_arithmetic_in_numbers(self) -> None:
        testcase: str = "-20 - 90"
        expected: int = -110
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_negative_arithmetic_in_words(self) -> None:
        testcase: str = "two hundred and twenty-four times two"
        expected: int = 448
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_points_arithmetic_in_numbers(self) -> None:
        testcase: str = "234.89 - 344.23"
        expected: float = -109.34
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_points_arithmetic_in_words(self) -> None:
        testcase: str = "ten point one six plus two thousand four hundred"
        expected: float = 2410.16
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_basic_arithmetic_in_mixed(self) -> None:
        testcase: str = "88 mod 19"
        expected: int = 12
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_point_arithmetic_in_mixed(self) -> None:
        testcase: str = "forty eight + sixty point three two"
        expected: float = 108.32
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_negative_arithmetic_in_mixed(self) -> None:
        testcase: str = "negative ninety eight * negative thirty three point three two"
        expected: float = 3265.36
        self.assertEqual(BasicCalculator(testcase).run().__round__(2), expected)

    def test_empty_string(self) -> None:
        testcase: str = ""
        expected: str = "Provide a valid equation (E.g. 12 + 30 or ten plus sixteen)"
        self.assertEqual(BasicCalculator(testcase).run(), expected)

    def test_words_not_numbers(self) -> None:
        testcase: str = "third times vowels"
        expected: str = "Please enter a valid number word."
        self.assertEqual(BasicCalculator(testcase).run(), expected)

    def test_numbers_not_figures(self) -> None:
        testcase: str = "20 + 20e3"
        expected: str = "Provide a valid equation (E.g. 12 + 30 or ten plus sixteen)"
        self.assertEqual(BasicCalculator(testcase).run(), expected)

    def test_dashes(self) -> None:
        testcase: str = "- / -"
        expected: str = "Provide a valid equation (E.g. 12 + 30 or ten plus sixteen)"
        self.assertEqual(BasicCalculator(testcase).run(), expected)

    def test_dots(self) -> None:
        testcase: str = "-2. / -2"
        expected: float = 1.0
        self.assertEqual(BasicCalculator(testcase).run(), expected)

    def test_one_operand(self) -> None:
        testcase: str = "-245.89 * "
        expected: str = "Provide a valid equation (E.g. 12 + 30 or ten plus sixteen)"
        self.assertEqual(BasicCalculator(testcase).run(), expected)


if __name__ == '__main__':
    unittest.main()
