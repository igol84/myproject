from contracts import contract
from money import Money  # pip install money  https://github.com/carlospalol/money
from decimal import Decimal
from currency import Currencies


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
>>> print(money_UAH.format('uk_UA'))                           # Get format price
1 750,50 ₴

>>> money_USD = MoneyMy.get_converted_money(money_UAH, currency_to='USD')     # New converted price+
>>> print(money_USD)
USD 63.65
>>> print(money_USD.UAH)                               # Get price in UAH
UAH 1,750.38
>>> print(money_USD.format('en_US'))                   # Get format price
$63.65
>>> print(money_USD.format_my())                       # Get format price
63.65$

>>> MoneyMy.currencies['UAH'].rate=35                      # Edit currency
>>> money_UAH = MoneyMy.get_converted_money(money_USD, currency_to='UAH')     # Reverse
>>> print(money_UAH)
UAH 2,227.75
>>> print(money_UAH.USD)                                       # Get price in USD
USD 63.65
>>> MoneyMy.currencies['UAH'].rate=29
>>> print(money_USD.UAH)                                       # Get price in UAH
UAH 1,845.85
>>> print(money_UAH.format_my())                               # Get price in UAH in formatting string
2,227.75₴

>>> money_CNY = MoneyMy.get_converted_money(money_USD, currency_to='CNY')     # USD -> CNY
>>> print(money_CNY.format_my())
394.63¥
>>> money_UAH = MoneyMy.get_converted_money(money_CNY, currency_to='UAH')     # CNY -> UAH
>>> print(money_UAH.format_my())
1,845.85₴

    """
    currencies = Currencies().get_currencies_for_test()  # currency : rate for 1 USD {'USD': 1, 'UAH': 27.5}
    default_currency = 'UAH'

    @contract
    def __init__(self, amount='0', currency: "str" = default_currency):
        assert currency in MoneyMy.currencies, f"'{self.__class__.__name__}' has no currency '{currency}'"
        Money.__init__(self, amount=amount, currency=currency)

    def __getattr__(self, item):
        """For get money in .USD or .UAH"""
        assert item in MoneyMy.currencies, f"'{self.__class__.__name__}' object has no attribute '{item}'"
        get_currency = item
        if get_currency == self.currency:
            return self
        else:
            return MoneyMy.get_converted_money(self, get_currency)

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
