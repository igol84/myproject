from dataclasses import field, InitVar, asdict

from decimal import Decimal

from pydantic.dataclasses import dataclass

from util.currency import Currency, get_currencies_for_test

# TODO: need to override this attribute
currencies: dict[str, Currency] = get_currencies_for_test()
default_currency = 'UAH'


@dataclass
class Money:
    """
>>> money_UAH = Money(1750.5)          # Create price
>>> print(money_UAH)                                           # Get price
Money(amount=1750.5, currency=Currency(code='UAH', rate=27.5, sign='₴'))
>>> print(money_UAH.amount)                                    # Get price amount
1750.5
>>> print(money_UAH.currency)                                  # Get price currency
Currency(code='UAH', rate=27.5, sign='₴')
>>> print(money_UAH.format())                           # Get format price
1,750.50₴
>>> print(asdict(money_UAH))
{'amount': 1750.5, 'currency': {'code': 'UAH', 'rate': 27.5, 'sign': '₴'}}
>>> money_USD = Money.get_converted_money(money_UAH, currency_to='USD')     # New converted price
>>> print(money_USD.format())
63.65$
>>> money_USD += 2
>>> print(money_USD.format())
65.65$
>>> money_USD -= 2
>>> print(money_USD.format())
63.65$
>>> money_USD *= 2
>>> print(money_USD.format())
127.30$
>>> money_UAH = Money.get_converted_money(money_USD, currency_to='UAH')
>>> print(money_UAH.format())
3,500.75₴
>>> money_UAH1 = Money(amount=50.5, currency=currencies['UAH'])
>>> money_UAH2 = Money(amount=40.5, currency=currencies['UAH'])
>>> print(money_UAH1 + money_UAH2)
Money(amount=91.0, currency=Currency(code='UAH', rate=27.5, sign='₴'))
>>> print(money_UAH1 + money_USD)
Money(amount=3551.25, currency=Currency(code='UAH', rate=27.5, sign='₴'))
    """
    amount: float = 0
    currency: Currency = currencies['UAH']

    def format(self) -> str:
        return f'{self.amount:,.2f}{self.currency.sign}'

    def __add__(self, other):
        if not isinstance(other, Money):
            amount = Decimal(self.amount) + Decimal(other)
        else:
            if self.currency.code == other.currency.code:
                amount = Decimal(self.amount) + Decimal(other.amount)
            else:
                amount = Decimal(self.amount) + Decimal(Money.get_converted_money(other, self.currency.code).amount)
        return Money(amount=amount, currency=self.currency)

    def __sub__(self, other):
        if not isinstance(other, Money):
            amount = Decimal(self.amount) - Decimal(other)
        else:
            if self.currency.code == other.currency.code:
                amount = Decimal(self.amount) - Decimal(other.amount)
            else:
                amount = Decimal(self.amount) - Decimal(Money.get_converted_money(other, self.currency.code).amount)
        return Money(amount=amount, currency=self.currency)

    def __mul__(self, other: float):
        amount = self.amount * other
        return Money(amount=amount, currency=self.currency)

    @classmethod
    def get_converted_money(cls, money: 'Money', currency_to: str) -> 'Money':
        assert currency_to in currencies, f"'{cls.__name__}' has no currency '{currency_to}'"
        if money.currency == currency_to:
            amount = money.amount
        else:
            amount = round(Decimal(money.amount) / Decimal(currencies[money.currency.code].rate)
                           * Decimal(currencies[currency_to].rate), 2)
        return Money(amount=float(amount), currency=currencies[currency_to])
