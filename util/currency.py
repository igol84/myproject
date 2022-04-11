from pydantic import constr, confloat
from pydantic.dataclasses import dataclass


@dataclass
class Currency:
    code: constr(regex=r'^\w{3}$')
    rate: confloat(gt=0)
    sign: constr(regex=r'^.$')

    def __post_init__(self):
        self.code = self.code.upper()


def get_currencies_for_test() -> dict[str, Currency]:
    currencies = {'USD': Currency(code='USD', rate=1, sign='$'), 'UAH': Currency(code='UAH', rate=27.5, sign='₴'),
                  'CNY': Currency(code='CNY', rate=6.2, sign='¥')}
    return currencies
