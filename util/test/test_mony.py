import unittest
from contracts import ContractNotRespected
from util.currency import Currency
from util.money_my import MoneyMy

# print( Currency(code='Usa', rate=27.5, sign='₴d'))

class TestInitMony(unittest.TestCase):

    def test_initial_01(self):
        UAH = Currency(code='UAH', rate=27.5, sign='₴')
        self.assertEqual(str(UAH), '<Currency UAH rate 27.5 ₴>')
        self.assertEqual(UAH.code, 'UAH')
        self.assertEqual(UAH.rate, 27.5)
        self.assertEqual(UAH.sign, '₴')

    def test_initial_02(self):
        UAH = Currency(code='UAH', rate=28, sign='₴')
        self.assertEqual(UAH.rate, 28)

    def test_contract_raises(self):
        self.assertRaises(ContractNotRespected, Currency, code='UA', rate=27.5, sign='₴')
        self.assertRaises(ContractNotRespected, Currency, code='UAH', rate="27.5", sign='₴')
        self.assertRaises(ContractNotRespected, Currency, code='UAH', rate=27.5, sign='₴3')

