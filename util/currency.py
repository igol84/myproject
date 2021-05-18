from typing import Union, Optional

from contracts import contract, new_contract


class Currency:
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
    """
    new_contract('code', 'str[3]')
    new_contract('rate', 'number, >0')
    new_contract('sign', 'str[<2]')

    @contract(code='code', rate='rate', sign='sign')
    def __init__(self, code: str, rate: Union[int, float], sign: str = ''):
        """
        :param code: str[3] ("UAH", "USD" ...)
        :param rate: int, float, >0  (27, 27.5)
        :param sign: str ('¥', '₴')
        """
        self._code = code.upper()
        self._rate = rate
        self._sign = sign

    @contract(code='code')
    def set_code(self, code: str) -> None:
        self._code = code

    def get_code(self) -> str:
        return self._code

    code = property(get_code, set_code)

    def get_rate(self) -> float:
        return self._rate

    @contract(rate='rate')
    def set_rate(self, rate):
        self._rate = float(rate)

    rate = property(get_rate, set_rate)

    @contract(sign='sign')
    def set_sign(self, sign):
        self._sign = sign

    def get_sign(self):
        return self._sign

    sign = property(get_sign, set_sign)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.code} rate {self.rate} {self.sign}>'


class Currencies(dict):
    """
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

    @contract(currencies='None | dict(str: $Currency)')
    def __init__(self, currencies: Optional[dict[str, Currency]] = None):
        """
        :param currencies: dict(str : Currency)
        """
        super().__init__()
        dict.__setitem__(self, 'USD', Currency(code='USD', rate=1, sign='$'))
        if currencies:
            self.update(currencies)

    @contract(currency='$Currency')
    def set_currency(self, currency: Currency) -> None:
        assert currency.code != 'USD', f"'{self.__class__.__name__}' already have currency 'USD'"
        dict.__setitem__(self, currency.code, currency)

    def __setitem__(self, key:str, currency:Currency) -> None:
        self.set_currency(currency)

    def get_currencies_for_test(self) -> 'Currencies':
        self.set_currency(Currency(code='UAH', rate=27.5, sign='₴'))
        self.set_currency(Currency(code='CNY', rate=6.2, sign='¥'))
        return self
