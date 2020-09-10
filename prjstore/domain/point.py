import datetime
from sale import Sale, Item, get_sale_for_test


class Point:
    """
>>> sale = get_sale_for_test()                                                    # Create sale
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
<SaleLineItem: item=<Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>, qty=1>
<SaleLineItem: item=<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=2>
<SaleLineItem: item=<Item: product=<Product: id=6, desc=item2, price=UAH 500.00>, qty=2>, qty=1>>
>>> point = Point('Бокс')
>>> point.make_new_sale()


    """
    def __init__(self, name):
        self._name = name
        self._sales = []

    def make_new_sale(self):
        pass
