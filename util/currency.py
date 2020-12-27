from contracts import contract, new_contract


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
>>> currencies['UAH'] = Currency(code='UAH', rate=25.5, sign='₴')
>>> currencies['UAH']
<Currency UAH rate 25.5 ₴>
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

    new_contract('code', lambda s: isinstance(s, str) and len(s) == 3)
    new_contract('rate', 'float|int, >0')
    new_contract('sign', lambda s: isinstance(s, str) and len(s) < 2)

    @contract(code='code', rate='rate', sign='sign')
    def __init__(self, code, rate, sign=''):
        """

        :param code: str, len(code) == 3 ("UAH", "USD" ...)
        :param rate: int, float, >0  (27, 27.5)
        :param sign: str ('¥', '₴')
        """
        self.__code = code.upper()
        self.__rate = rate
        self.__sign = sign
    @contract(code='code')
    def set_code(self, code):
        self.__code = code

    def get_code(self):
        return self.__code

    code = property(get_code, set_code)

    def get_rate(self):
        return self.__rate

    @contract(rate='rate')
    def set_rate(self, rate):
        self.__rate = rate

    rate = property(get_rate, set_rate)

    def get_sign(self):
        return self.__sign

    @contract(sign='sign')
    def set_sign(self, sign):
        self.__sign = sign

    sign = property(get_sign, set_sign)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.code} rate {self.rate} {self.sign}>'
