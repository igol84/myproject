from contracts import contract
from money import Money  # pip install money  https://github.com/carlospalol/money
from decimal import Decimal
from currency import Currencies


class MoneyMy(Money):
    """
>>> money = MoneyMy(amount=1750.5, currency='UAH')          # Create price
>>>
>>> print(money)                                           # Get price
UAH 1,750.50

>>> print(money.amount)                                    # Get price amount
1750.5
>>> print(money.currency)                                  # Get price currency
UAH
>>> print(money.USD)                                       # Get price in USD
USD 63.65
>>> print(money.format('uk_UA'))                           # Get format price
1 750,50 ₴

>>> convert_money = MoneyMy.get_converted_money(money)     # New converted price+
>>> print(convert_money)
USD 63.65
>>> print(convert_money.UAH)                               # Get price in UAH
UAH 1,750.38
>>> print(convert_money.format('en_US'))                   # Get format price
$63.65
>>> MoneyMy.currencies['UAH'].rate=35                           # Edit currency
>>> money = MoneyMy.get_converted_money(convert_money)     # Reverse
>>> print(money)
UAH 2,227.75
>>> print(money.USD)                                       # Get price in USD
USD 63.65
>>> print(money.USD.format_my())                           # Get price in USD in formatting string
63.65$
>>> MoneyMy.currencies['UAH'].rate=29
>>> print(convert_money.UAH)                               # Get price in UAH
UAH 1,845.85
>>> print(money.format_my())                               # Get price in UAH in formatting string
2,227.75₴
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
    def get_converted_money(cls, money_my: "isinstance(MoneyMy)", to_currency: 'str' = ''):
        """"USD -> UAH or UAH -> USD"""
        assert to_currency == '' or to_currency in cls.currencies, f"'{cls.__name__}' has no currency '{to_currency}'"
        to_currency = to_currency if to_currency else (set(money_my.currencies) - {money_my.currency}).pop()
        if money_my.currency == 'UAH' and to_currency == 'USD':
            amount = round(money_my.amount / Decimal(money_my.currencies['UAH'].rate), 2)
        elif money_my.currency == 'USD' and to_currency == 'UAH':
            amount = round(money_my.amount * Decimal(money_my.currencies['UAH'].rate), 2)
        else:  # money_my.currency == to_currency
            amount = money_my.amount
        return MoneyMy(amount=amount, currency=to_currency)
