import unittest
from contracts import ContractNotRespected
from util.currency import Currency, Currencies


class Test_01_InitCurrency(unittest.TestCase):

    def test_initial_01(self):
        UAH = Currency(code='uah', rate=27.5, sign='₴')
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


class TestCurrencies(unittest.TestCase):
    def setUp(self):
        currencies = {'UAH': Currency(code='UAH', rate=27.5, sign='₴'),
                      'CNY': Currency(code='CNY', rate=6.2, sign='¥')}
        self.currencies = Currencies(currencies)


class Test_02_InitCurrencies(TestCurrencies):
    def test_01_initial(self):
        self.assertEqual(str(self.currencies), "{"
                                               "'USD': <Currency USD rate 1 $>, "
                                               "'UAH': <Currency UAH rate 27.5 ₴>, "
                                               "'CNY': <Currency CNY rate 6.2 ¥>"
                                               "}")
        self.assertEqual(str(self.currencies['USD']), '<Currency USD rate 1 $>')
        self.assertEqual(str(self.currencies['UAH']), '<Currency UAH rate 27.5 ₴>')
        self.assertIn('CNY', self.currencies)

    def test_02_add_currency(self):
        with self.assertRaises(KeyError):
            print(self.currencies['EUR'])
        EUR = Currency(code='EUR', rate=32, sign='€')
        self.currencies.set_currency(EUR)
        self.assertEqual(str(self.currencies['EUR']), '<Currency EUR rate 32 €>')

    def test_03_del_currency(self):
        del(self.currencies['CNY'])
        self.assertEqual(str(self.currencies), "{"
                                               "'USD': <Currency USD rate 1 $>, "
                                               "'UAH': <Currency UAH rate 27.5 ₴>"
                                               "}")

    def test_04_contract_raises(self):
        self.currencies['UAH'] = Currency(code='UAH', rate=25.5, sign='₴')
        self.assertEqual(str(self.currencies['UAH']), "<Currency UAH rate 25.5 ₴>")
        self.assertRaises(ContractNotRespected, self.currencies.set_currency, 'UAH')
