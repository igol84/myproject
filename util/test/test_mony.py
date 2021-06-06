import unittest
from contracts import ContractNotRespected
from pydantic import ValidationError

from util.money import Money, currencies


class Test_MyMoney(unittest.TestCase):
    def setUp(self):
        self.money_UAH = Money(amount=1750.5, currency=currencies['UAH'])

    def test_01_initial(self):
        self.assertEqual(self.money_UAH.amount, 1750.5)
        self.assertEqual(self.money_UAH.currency.code, 'UAH')
        self.assertEqual(str(self.money_UAH.format()), '1,750.50₴')

    def test_02_converted(self):
        money_USD = Money.get_converted_money(self.money_UAH, currency_to='USD')
        self.assertEqual(str(money_USD.format()), '63.65$')

    def test_03_edit_currency(self):
        dump_cur = currencies['UAH'].rate
        currencies['UAH'].rate = 35
        money_USD = Money.get_converted_money(self.money_UAH, currency_to='USD')
        self.assertEqual(str(money_USD.format()), '50.01$')
        currencies['UAH'].rate = dump_cur

    def test_04_another_currency(self):
        self.money_CNY = Money.get_converted_money(self.money_UAH, currency_to='CNY')
        self.assertEqual(str(self.money_CNY.format()), '394.66¥')
        self.money_UAH = Money.get_converted_money(self.money_CNY, currency_to='UAH')
        self.assertEqual(str(self.money_UAH.format()), '1,750.51₴')
        self.money_UAH = Money.get_converted_money(self.money_UAH, currency_to='UAH')
        self.assertEqual(str(self.money_UAH.format()), '1,750.51₴')

    def test_05_contract_raises(self):
        self.assertRaises(ValidationError, Money, amount="df", currency=currencies['UAH'])

    def test_06_add(self):
        self.money_UAH += 20
        self.assertEqual(str(self.money_UAH.amount), '1770.5')
        money_UAH2 = Money(amount=20.5, currency=currencies['UAH'])
        money_UAH3 = self.money_UAH + money_UAH2
        self.assertEqual(str(money_UAH3.amount), '1791.0')
        money_USD2 = Money(amount=20.5, currency=currencies['USD'])
        money_UAH4 = self.money_UAH + money_USD2
        self.assertEqual(str(money_UAH4.amount), '2334.25')
