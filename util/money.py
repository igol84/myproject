from decimal import Decimal

from pydantic.dataclasses import dataclass

from util.currency import Currency, get_currencies_for_test


@dataclass
class Money:
    # TODO: need to override this attribute
    currencies = get_currencies_for_test()
    default_currency = 'UAH'

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
        assert currency_to in Money.currencies, f"'{cls.__name__}' has no currency '{currency_to}'"
        if money.currency == currency_to:
            amount = money.amount
        else:
            amount = round(Decimal(money.amount) / Decimal(Money.currencies[money.currency.code].rate)
                           * Decimal(Money.currencies[currency_to].rate), 2)
        return Money(amount=float(amount), currency=Money.currencies[currency_to])
