import unittest
from contracts import ContractNotRespected
from util.currency import Currency, Currencies
from util.money_my import MoneyMy


class Test_01_InitMyMoney(unittest.TestCase):
    def setUp(self):
        currencies = {'UAH': Currency(code='UAH', rate=27.5, sign='₴'),
                      'CNY': Currency(code='CNY', rate=6.2, sign='¥')}
        MoneyMy.currencies = Currencies(currencies)
        self.money_UAH = MoneyMy(amount=1750.5, currency='UAH')

    def test_01_initial(self):
        money_UAH = self.money_UAH
        self.assertEqual(str(money_UAH), 'UAH 1,750.50')
        self.assertEqual(money_UAH.amount, 1750.5)
        self.assertEqual(money_UAH.currency, 'UAH')
        self.assertEqual(str(money_UAH.USD), 'USD 63.65')
        self.assertEqual(str(money_UAH.format_my()), '1,750.5₴')
        self.assertEqual(str(money_UAH.format('uk_UA')), '1 750,50 ₴')  # 1 750,50 ₴

    def test_02_converted(self):
        money_UAH = self.money_UAH
        money_USD = MoneyMy.get_converted_money(money_UAH, currency_to='USD')
        self.assertEqual(str(money_USD), 'USD 63.65')
        self.assertEqual(str(money_USD.UAH), 'UAH 1,750.38')
        self.assertEqual(str(money_USD.format('en_US')), '$63.65')
        self.assertEqual(str(money_USD.format_my()), '63.65$')
        self.assertEqual(str(money_USD.UAH.format_my()), '1,750.38₴')

    def test_03_edit_currency(self):
        money_UAH = self.money_UAH
        MoneyMy.currencies['UAH'].rate = 35
        money_USD = MoneyMy.get_converted_money(money_UAH, currency_to='USD')
        self.assertEqual(str(money_USD), 'USD 50.01')
        self.assertEqual(str(money_USD.UAH), 'UAH 1,750.35')

    def test_04_another_currency(self):
        money_UAH = self.money_UAH
        money_CNY = MoneyMy.get_converted_money(money_UAH, currency_to='CNY')
        self.assertEqual(str(money_CNY), 'CNY 394.66')
        money_UAH = MoneyMy.get_converted_money(money_CNY, currency_to='UAH')
        self.assertEqual(str(money_UAH), 'UAH 1,750.51')
        money_UAH = MoneyMy.get_converted_money(money_UAH, currency_to='UAH')
        self.assertEqual(str(money_UAH), 'UAH 1,750.51')

    def test_05_contract_raises(self):
        self.assertRaises(ContractNotRespected, MoneyMy, amount=1750.5, currency='UA')
        self.assertRaises(ValueError, MoneyMy, amount="df", currency='UAH')
