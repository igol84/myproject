from contracts import contract


class Currencies(dict):
    """
>>> UAH = Currency(code='UAH', rate=27.5, sign='₴')
>>> UAH
<Currency UAH rate 27.5 ₴>
>>> UAH.code
'UAH'
>>> UAH.rate
27.5
>>> UAH.sign
'₴'
>>> currencies = Currencies().get_currencies_for_test()
>>> currencies
{'USD': <Currency USD rate 1 $>, 'UAH': <Currency UAH rate 27.5 ₴>, 'CNY': <Currency CNY rate 6.2 ¥>}
>>> 'UAH' in  currencies
True
>>> currencies['USD']
<Currency USD rate 1 $>
    """

    def __init__(self):
        super().__init__()
        dict.__setitem__(self, 'USD', Currency(code='USD', rate=1, sign='$'))

    @contract
    def set_currency(self, currency: "isinstance(Currency)"):
        assert currency.code != 'USD', f"'{self.__class__.__name__}' already have currency 'USD'"
        dict.__setitem__(self, currency.code, currency)

    def __setitem__(self, key, value):
        self.set_currency(value)

    def get_currencies_for_test(self):
        self.set_currency(Currency(code='UAH', rate=27.5, sign='₴'))
        self.set_currency(Currency(code='CNY', rate=6.2, sign='¥'))
        return self


class Currency:
    """

    """

    @contract
    def __init__(self, code: 'str', rate: "float|int, >0", sign=''):
        self.code = code
        self.rate = rate
        self.sign = sign

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.code} rate {self.rate} {self.sign}>'
