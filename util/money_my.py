"""
    >>> money = MoneyMy(amount=750.5, currency='UAH')  # Create price
    >>> print(money)                                   # Get price
    UAH 750.50
    >>> print(money.amount)                            # Get price amount
    750.5
    >>> print(money.currency)                          # Get price currency
    UAH
    >>> print(money.format('uk_UA'))                          # Get price currency
    750,50 ₴
"""

from money import Money  # pip install money  https://github.com/carlospalol/money
from decimal import Decimal

class MoneyMy(Money):
    default_currency = 'UAH'
    rate_USD_to_UAH = 27.5
    rate_UAH_to_USD = 1/rate_USD_to_UAH

    def convert(self):
        pass