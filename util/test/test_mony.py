import unittest
from contracts import ContractNotRespected
from util.currency import Currency, Currencies
from util.money_my import MoneyMy
from util.test.test_currecy import TestCurrencies


class Test_MyMoney(unittest.TestCase):
    def setUp(self):
        testCurrencies = TestCurrencies()
        testCurrencies.setUp()
        self.money_UAH = MoneyMy(amount=1750.5, currency='UAH')
        MoneyMy.currencies = Currencies(testCurrencies.currencies)

    def test_01_initial(self):
        self.assertEqual(str(self.money_UAH), 'UAH 1,750.50')
        self.assertEqual(self.money_UAH.amount, 1750.5)
        self.assertEqual(self.money_UAH.currency, 'UAH')
        self.assertEqual(str(self.money_UAH.USD), 'USD 63.65')
        self.assertEqual(str(self.money_UAH.format_my()), '1,750.5₴')
        self.assertEqual(str(self.money_UAH.format('uk_UA')), '1 750,50 ₴')  # 1 750,50 ₴

    def test_02_converted(self):
        money_USD = MoneyMy.get_converted_money(self.money_UAH, currency_to='USD')
        self.assertEqual(str(money_USD), 'USD 63.65')
        self.assertEqual(str(money_USD.UAH), 'UAH 1,750.38')
        self.assertEqual(str(money_USD.format('en_US')), '$63.65')
        self.assertEqual(str(money_USD.format_my()), '63.65$')
        self.assertEqual(str(money_USD.UAH.format_my()), '1,750.38₴')

    def test_03_edit_currency(self):
        MoneyMy.currencies['UAH'].rate = 35
        money_USD = MoneyMy.get_converted_money(self.money_UAH, currency_to='USD')
        self.assertEqual(str(money_USD), 'USD 50.01')
        self.assertEqual(str(money_USD.UAH), 'UAH 1,750.35')

    def test_04_another_currency(self):
        self.money_CNY = MoneyMy.get_converted_money(self.money_UAH, currency_to='CNY')
        self.assertEqual(str(self.money_CNY), 'CNY 394.66')
        self.money_UAH = MoneyMy.get_converted_money(self.money_CNY, currency_to='UAH')
        self.assertEqual(str(self.money_UAH), 'UAH 1,750.51')
        self.money_UAH = MoneyMy.get_converted_money(self.money_UAH, currency_to='UAH')
        self.assertEqual(str(self.money_UAH), 'UAH 1,750.51')

    def test_05_contract_raises(self):
        self.assertRaises(ContractNotRespected, MoneyMy, amount=1750.5, currency='UA')
        self.assertRaises(ValueError, MoneyMy, amount="df", currency='UAH')
