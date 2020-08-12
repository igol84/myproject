from contracts import contract
from money import Money  # pip install money  https://github.com/carlospalol/money
from decimal import Decimal


class MoneyMy(Money):
    """
>>> money = MoneyMy(amount=750.5, currency='UAH')          # Create price
>>> print(money)                                           # Get price
UAH 750.50

>>> print(money.amount)                                    # Get price amount
750.5
>>> print(money.currency)                                  # Get price currency
UAH
>>> print(money.USD)                                       # Get price in USD
USD 27.29
>>> print(money.format('uk_UA'))                           # Get format price
750,50 ₴

>>> convert_money = MoneyMy.get_converted_money(money)     # New converted price+
>>> print(convert_money)
USD 27.29
>>> print(convert_money.UAH)                               # Get price in UAH
UAH 750.48
>>> print(convert_money.format('en_US'))                   # Get format price
$27.29
>>> money = MoneyMy.get_converted_money(convert_money)     # Reverse
>>> print(money)
UAH 750.48
    """
    currencies = {'USD': 1, 'UAH': 27.5}  # currency : rate for 1 USD
    default_currency = 'UAH'

    def __init__(self, amount='0', currency=default_currency):
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

    @classmethod
    @contract
    def get_converted_money(cls, money_my: "isinstance(MoneyMy)", to_currency: 'str' = ''):
        """"USD -> UAH or UAH -> USD"""
        assert to_currency == '' or to_currency in cls.currencies, f"'{cls.__name__}' has no currency '{to_currency}'"
        to_currency = to_currency if to_currency else (set(money_my.currencies) - {money_my.currency}).pop()
        if money_my.currency == 'UAH' and to_currency == 'USD':
            amount = round(money_my.amount / Decimal(money_my.currencies['UAH']), 2)
        elif money_my.currency == 'USD' and to_currency == 'UAH':
            amount = round(money_my.amount * Decimal(money_my.currencies['UAH']), 2)
        else: # money_my.currency == to_currency
            amount = money_my.amount
        return MoneyMy(amount=amount, currency=to_currency)
