from money import Money  # pip install money  https://github.com/carlospalol/money
from decimal import Decimal


class MoneyMy(Money):
    """
>>> money = MoneyMy(amount=750.5, currency='UAH')  # Create price
>>> print(money)                                   # Get price
UAH 750.50
>>> print(money.USD)                                   # Get price
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
>>> print(convert_money.UAH)
UAH 750.48
>>> print(convert_money.format('en_US'))           # Get format price
$27.29
>>> money = MoneyMy.get_converted_money(convert_money)     # Reverse
>>> print(money)
UAH 750.48
    """
    default_currency = 'UAH'
    rate_USD_to_UAH = 27.5

    def USD(self):
        if self.currency == 'USD':
            return self
        elif self.currency == 'UAH':
            return MoneyMy.get_converted_money(self)

    USD = property(USD)

    def UAH(self):
        if self.currency == 'UAH':
            return self
        elif self.currency == 'USD':
            return MoneyMy.get_converted_money(self)

    UAH = property(UAH)

    @staticmethod
    def get_converted_money(money) -> 'MoneyMy':
        if money.currency == 'UAH':
            currency = 'USD'
            amount = round(money.amount / Decimal(money.rate_USD_to_UAH), 2)
        else:
            currency = 'UAH'
            amount = round(money.amount * Decimal(money.rate_USD_to_UAH), 2)
        return MoneyMy(amount=amount, currency=currency)
