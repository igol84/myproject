from pydantic import constr, confloat
from pydantic.dataclasses import dataclass


@dataclass
class Currency:
    """
>>> UAH = Currency(code='uah', rate=27.5, sign='₴')
>>> UAH
Currency(code='UAH', rate=27.5, sign='₴')
>>> UAH.code
'UAH'
>>> UAH.rate
27.5
>>> UAH.sign
'₴'
>>> currencies: dict[str, Currency] = get_currencies_for_test()
>>> currencies
{\
'USD': Currency(code='USD', rate=1.0, sign='$'), \
'UAH': Currency(code='UAH', rate=27.5, sign='₴'), \
'CNY': Currency(code='CNY', rate=6.2, sign='¥')\
}
>>> 'USD' in currencies
True
    """
    code: constr(regex=r'^\w{3}$')
    rate: confloat(gt=0)
    sign: constr(regex=r'^.$')

    def __post_init__(self):
        self.code = self.code.upper()


def get_currencies_for_test() -> dict[str, Currency]:
    currencies = {'USD': Currency(code='USD', rate=1, sign='$'), 'UAH': Currency(code='UAH', rate=27.5, sign='₴'),
                  'CNY': Currency(code='CNY', rate=6.2, sign='¥')}
    return currencies
