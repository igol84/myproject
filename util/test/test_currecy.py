import unittest
from pydantic import ValidationError

from util.currency import Currency


class Test_01_Currency(unittest.TestCase):

    def setUp(self):
        self.cur = Currency(code='uah', rate=27.5, sign='₴')

    def test_01_initial(self):
        self.assertEqual(str(self.cur), "Currency(code='UAH', rate=27.5, sign='₴')")
        self.assertEqual(self.cur.code, 'UAH')
        self.assertEqual(self.cur.rate, 27.5)
        self.assertEqual(self.cur.sign, '₴')

    def test_02_edit_code(self):
        self.cur.code = 'USD'
        self.assertEqual(str(self.cur), "Currency(code='USD', rate=27.5, sign='₴')")

    def test_03_edit_rate(self):
        self.cur.rate = 28
        self.assertEqual(str(self.cur), "Currency(code='UAH', rate=28, sign='₴')")
        self.cur.rate = 28.5
        self.assertEqual(str(self.cur), "Currency(code='UAH', rate=28.5, sign='₴')")

    def test_04_edit_sign(self):
        self.cur.sign = '¥'
        self.assertEqual(str(self.cur), "Currency(code='UAH', rate=27.5, sign='¥')")

    def test_contract_raises(self):
        self.assertRaises(ValidationError, Currency, code='UA', rate=27.5, sign='₴')
        self.assertRaises(ValidationError, Currency, code='UAH', rate=27.5, sign='₴3')