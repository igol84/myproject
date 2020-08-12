from money import Money  # pip install money  https://github.com/carlospalol/money
from decimal import Decimal


class MoneyMy(Money):
    """
>>> money = MoneyMy(amount=750.5, currency='UAH')  # Create price
>>> print(money)                                   # Get price
UAH 750.50
>>> print(money.USD)                               # Get price in USD
USD 27.29
>>> print(money.amount)                            # Get price amount
750.5
>>> print(money.currency)                          # Get price currency
UAH
>>> print(money.format('uk_UA'))                   # Get format price
750,50 ₴

>>> convert_money = MoneyMy.get_converted_money(money)     # New converted price+
>>> print(convert_money)
USD 27.29
>>> print(convert_money.UAH)                       # Get price in UAH
UAH 750.48
>>> print(convert_money.format('en_US'))           # Get format price
$27.29
>>> money = MoneyMy.get_converted_money(convert_money)     # Reverse
>>> print(money)
UAH 750.48
    """
    currencies = ['UAH', 'USD']
    default_currency = currencies[0]
    rate_USD_to_UAH = 27.5

    def __getattr__(self, item):
        """For get money in .USD or .UAH"""
        if item in MoneyMy.currencies:
            get_currency = item
            if get_currency == self.currency:
                return self
            else:
                return MoneyMy.get_converted_money(self, get_currency)
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    @classmethod
    def get_converted_money(cls, money_my, to_currency=None) -> 'MoneyMy':
        if money_my.currency == 'UAH':
            to_currency = 'USD'
            amount = round(money_my.amount / Decimal(money_my.rate_USD_to_UAH), 2)
        else:
            to_currency = 'UAH'
            amount = round(money_my.amount * Decimal(money_my.rate_USD_to_UAH), 2)
        return MoneyMy(amount=amount, currency=to_currency)


if __name__ == '__main__':
    money = MoneyMy(amount=750.5, currency='UAH')  # Create price
    print(money)  # Get price
    print(money.USD)  # Get price in USD
