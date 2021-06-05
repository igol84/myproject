import unittest
from contracts import ContractNotRespected
from util.currency import Currencies
from util.money_my import Money
from util.test.test_currecy import TestCurrencies


class Test_MyMoney(unittest.TestCase):
    def setUp(self):
        testCurrencies = TestCurrencies()
        testCurrencies.setUp()
        self.money_UAH = Money(amount=1750.5, currency='UAH')
        Money.currencies = Currencies(testCurrencies.currencies)

    def test_01_initial(self):
        self.assertEqual(str(self.money_UAH), 'UAH 1,750.50')
        self.assertEqual(self.money_UAH.amount, 1750.5)
        self.assertEqual(self.money_UAH.currency, 'UAH')
        self.assertEqual(str(self.money_UAH.USD), 'USD 63.65')
        self.assertEqual(str(self.money_UAH.format()), '1,750.50₴')

    def test_02_converted(self):
        money_USD = Money.get_converted_money(self.money_UAH, currency_to='USD')
        self.assertEqual(str(money_USD), 'USD 63.65')
        self.assertEqual(str(money_USD.UAH), 'UAH 1,750.38')
        self.assertEqual(str(money_USD.format()), '63.65$')
        self.assertEqual(str(money_USD.UAH.format()), '1,750.38₴')

    def test_03_edit_currency(self):
        Money.currencies['UAH'].rate = 35
        money_USD = Money.get_converted_money(self.money_UAH, currency_to='USD')
        self.assertEqual(str(money_USD), 'USD 50.01')
        self.assertEqual(str(money_USD.UAH), 'UAH 1,750.35')

    def test_04_another_currency(self):
        self.money_CNY = Money.get_converted_money(self.money_UAH, currency_to='CNY')
        self.assertEqual(str(self.money_CNY), 'CNY 394.66')
        self.money_UAH = Money.get_converted_money(self.money_CNY, currency_to='UAH')
        self.assertEqual(str(self.money_UAH), 'UAH 1,750.51')
        self.money_UAH = Money.get_converted_money(self.money_UAH, currency_to='UAH')
        self.assertEqual(str(self.money_UAH), 'UAH 1,750.51')

    def test_05_contract_raises(self):
        self.assertRaises(ContractNotRespected, Money, amount=1750.5, currency='UA')
        self.assertRaises(ContractNotRespected, Money, amount="df", currency='UAH')

    def test_06_add(self):
        self.money_UAH += 20
        self.assertEqual(str(self.money_UAH.amount), '1770.5')
        money_UAH2 = Money(amount=20.5, currency='UAH')
        money_UAH3 = self.money_UAH + money_UAH2
        self.assertEqual(str(money_UAH3.amount), '1791.0')
        money_USD2 = Money(amount=20.5, currency='USD')
        money_UAH4 = self.money_UAH + money_USD2
        self.assertEqual(str(money_UAH4.amount), '2334.25')
