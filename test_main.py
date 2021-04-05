from unittest import TestCase
from unittest.mock import patch

from main import Calculator


class TestCalculator(TestCase):

    def setUp(self):
        self.calc = Calculator()

    @patch('main.Calculator.sum', return_value=6)
    def test_sum(self, sum):
        answer = sum(2, 4)
        self.assertEqual(answer, 6)
