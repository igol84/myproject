from typing import Union

from contracts import contract
from decimal import Decimal

from util.currency import Currencies


class Money():
    """
>>> money_UAH = Money(amount=1750.5, currency='UAH')          # Create price
>>>
>>> print(money_UAH)                                           # Get price
UAH 1,750.50
>>> print(money_UAH.amount)                                    # Get price amount
1750.5
>>> print(money_UAH.currency)                                  # Get price currency
UAH
>>> print(money_UAH.USD)                                       # Get price in USD
USD 63.65
>>> print(money_UAH.format())                           # Get format price
1,750.50₴
>>> money_USD = Money.get_converted_money(money_UAH, currency_to='USD')     # New converted price
>>> print(money_USD)
USD 63.65
>>> money_USD += 2
>>> print(money_USD)
USD 65.65
>>> money_USD -= 2
>>> print(money_USD)
USD 63.65
>>> money_USD *= 2
>>> print(money_USD)
USD 127.30
>>> money_UAH = Money.get_converted_money(money_USD, currency_to='UAH')
>>> print(money_UAH)
UAH 3,500.75
>>> money_UAH1 = Money(amount=50.5, currency='UAH')
>>> money_UAH2 = Money(amount=40.5, currency='UAH')
>>> print(money_UAH1 + money_UAH2)
UAH 91.00
>>> print(money_UAH1 + money_USD)
UAH 3,551.25


    """
    # TODO: need to override this attribute
    currencies = Currencies().get_currencies_for_test()
    default_currency = 'UAH'

    @contract(amount='int | float | $Decimal', currency='str[3]')
    def __init__(self, amount: Union[int, float, Decimal], currency: str = default_currency):
        """
        :param amount: int, float, Decimal
        :param currency: str[3] ("UAH", "USD" ...)
        """
        assert currency in Money.currencies, f"'{self.__class__.__name__}' has no currency '{currency}'"
        self.__amount = Decimal(amount)
        self.__currency = currency

    def __get_amount(self):
        return self.__amount

    @contract(amount='int | float | $Decimal')
    def __set_amount(self, amount):
        self.__amount = Decimal(amount)

    amount = property(__get_amount, __set_amount)

    def __get_currency(self):
        return self.__currency

    @contract(currency=str)
    def __set_currency(self, currency):
        self.__currency = currency

    currency = property(__get_currency, __set_currency)

    def __getattr__(self, currency: str) -> 'Money':
        """For get money in .USD or .UAH"""
        assert currency in Money.currencies, f"'{self.__class__.__name__}' has no currency '{currency}'"
        if currency == self.currency:
            return self
        else:
            return Money.get_converted_money(self, currency)

    def format(self) -> str:
        return f'{self.amount:,.2f}{self.currencies[self.currency].sign}'

    def __repr__(self):
        return f'{self.currency} {self.amount:,.2f}'  # 'UAH 1,750.50'

    @contract(other='int | float | $Decimal | Money')
    def __add__(self, other):
        if not isinstance(other, Money):
            amount = self.__amount + Decimal(other)
        else:
            if self.currency == other.currency:
                amount = self.__amount + other.__amount
            else:
                amount = self.__amount + Money.get_converted_money(other, self.currency).amount
        return Money(amount=amount, currency=self.currency)


    def __sub__(self, other):
        if not isinstance(other, Money):
            amount = self.__amount - Decimal(other)
        else:
            if self.currency == other.currency:
                amount = self.__amount - other.__amount
            else:
                amount = self.__amount - Money.get_converted_money(other, self.currency).amount
        return Money(amount=amount, currency=self.currency)

    def __mul__(self, other: int):
        amount = self.__amount * other
        return Money(amount=amount, currency=self.currency)

    @classmethod
    @contract(money='isinstance(Money)', currency_to='str')
    def get_converted_money(cls, money: 'Money', currency_to: str) -> 'Money':
        assert currency_to in cls.currencies, f"'{cls.__name__}' has no currency '{currency_to}'"
        if money.currency == currency_to:
            amount = money.amount
        else:
            amount = round(money.amount / Decimal(money.currencies[money.currency].rate)
                           * Decimal(money.currencies[currency_to].rate), 2)
        return Money(amount=amount, currency=currency_to)
