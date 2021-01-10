from contracts import contract
from money import Money  # pip install money  https://github.com/carlospalol/money
from decimal import Decimal

from util.currency import Currencies


class MoneyMy(Money):
    """
>>> money_UAH = MoneyMy(amount=1750.5, currency='UAH')          # Create price
>>>
>>> print(money_UAH)                                           # Get price
UAH 1,750.50
>>> print(money_UAH.amount)                                    # Get price amount
1750.5
>>> print(money_UAH.currency)                                  # Get price currency
UAH
>>> print(money_UAH.USD)                                       # Get price in USD
USD 63.65
>>> print(money_UAH.format('uk_UA'))                           # Get format price - 1 750,50 ₴
1 750,50 ₴
>>> print(money_UAH.format_my())                           # Get format price
1,750.5₴
>>> money_USD = MoneyMy.get_converted_money(money_UAH, currency_to='USD')     # New converted price
>>> print(money_USD)
USD 63.65

    """
    # TODO: need to override this attribute
    currencies = Currencies().get_currencies_for_test()
    default_currency = 'UAH'

    @contract(currency='str[3]')
    def __init__(self, amount='0', currency=default_currency):
        """
        :param amount: int, float, Decimal
        :param currency: str[3] ("UAH", "USD" ...)
        """
        assert currency in MoneyMy.currencies, f"'{self.__class__.__name__}' has no currency '{currency}'"
        Money.__init__(self, amount=amount, currency=currency)

    def __getattr__(self, currency):
        """For get money in .USD or .UAH"""
        assert currency in MoneyMy.currencies, f"'{self.__class__.__name__}' has no currency '{currency}'"
        if currency == self.currency:
            return self
        else:
            return MoneyMy.get_converted_money(self, currency)

    def format_my(self):
        return f'{self.amount:,}{self.currencies[self.currency].sign}'

    @classmethod
    @contract
    def get_converted_money(cls, money_my: "isinstance(MoneyMy)", currency_to: 'str') -> "isinstance(MoneyMy)":
        assert currency_to in cls.currencies, f"'{cls.__name__}' has no currency '{currency_to}'"
        if money_my.currency == currency_to:
            amount = money_my.amount
        else:
            amount = round(money_my.amount / Decimal(money_my.currencies[money_my.currency].rate)
                           * Decimal(money_my.currencies[currency_to].rate), 2)
        return MoneyMy(amount=amount, currency=currency_to)
