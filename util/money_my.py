from money import Money  # pip install money  https://github.com/carlospalol/money
from decimal import Decimal


class MoneyMy(Money):
    """
        >>> money = MoneyMy(amount=750.5, currency='UAH')  # Create price
        >>> print(money)                                   # Get price
        UAH 750.50
        >>> print(money.amount)                            # Get price amount
        750.5
        >>> print(money.currency)                          # Get price currency
        UAH
        >>> print(money.format('uk_UA'))                   # Get format price
        750,50 ₴

        >>> convert_money = MoneyMy.get_converted_money(money)     # New converted price+
        >>> print(convert_money)
        USD 27.29
        >>> print(convert_money.format('en_US'))           # Get format price
        $27.29
        >>> money = MoneyMy.get_converted_money(convert_money)     # Reverse
        >>> print(money)
        UAH 750.50
    """
    default_currency = 'UAH'
    rate_USD_to_UAH = 27.5

    @staticmethod
    def get_converted_money(money):
        if money.currency == 'UAH':
            currency = 'USD'
            amount = money.amount / Decimal(money.rate_USD_to_UAH)
        else:
            currency = 'UAH'
            amount = money.amount * Decimal(money.rate_USD_to_UAH)
        return MoneyMy(amount=amount, currency=currency)
