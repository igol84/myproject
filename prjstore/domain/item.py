from contracts import contract

from prjstore.domain.product_catalog import get_products_for_test
from prjstore.domain.abstract_product import AbstractProduct
from util.money_my import MoneyMy, Decimal

class Item:
    """
>>> test_product_catalog=get_products_for_test() # Get test product catalog
>>> test_product_catalog
[<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0, length_of_insole=11.0, width=Medium>,\
 <SimpleProduct: id=2, name=item23, price=UAH 600.00>,\
 <Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0, width=Medium>,\
 <SimpleProduct: id=4, name=item5, price=UAH 300.00>,\
 <SimpleProduct: id=6, name=item2, price=UAH 500.00>]

>>> item = Item(pr=test_product_catalog['2'], qty=3)              # Create new item
>>> item                                                          # get item
<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>
>>> item.product                                                  # get items product
<SimpleProduct: id=2, name=item23, price=UAH 600.00>
>>> item.product=test_product_catalog['3']                        # edit items product
>>> item.product
<Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0, width=Medium>
>>> item.qty                                                      # get items quantity
3
>>> item.qty=2                                                    # edit items quantity
>>> item.qty
2
>>> item.buy_price=100                                                    # edit items quantity
>>> item.buy_price
UAH 100

    """
    _default_curr = MoneyMy.default_currency

    def __init__(self, pr, qty=1, buy_price=0, currency=_default_curr):
        self.product = pr
        self.qty = qty
        self.set_buy_price(buy_price, currency)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: product={self._product}, qty={self._qty}>'

    def get_product(self) -> AbstractProduct:
        return self._product

    @contract(pr=AbstractProduct)
    def set_product(self, pr) -> None:
        self._product = pr

    product = property(get_product, set_product)

    def get_qty(self) -> int:
        return self._qty

    @contract(qty='int, >0')
    def set_qty(self, qty) -> None:
        self._qty = qty

    qty = property(get_qty, set_qty)

    def get_buy_price(self) -> MoneyMy:
        return self._buy_price

    @contract(buy_price='$MoneyMy | int | float | $Decimal', currency='None | str')
    def set_buy_price(self, buy_price, currency=None) -> None:
        if isinstance(buy_price, MoneyMy):
            self._buy_price = buy_price
        else:
            curr = currency if currency else self._buy_price.currency
            self._buy_price = MoneyMy(amount=str(buy_price), currency=curr)

    buy_price = property(get_buy_price, set_buy_price)


def get_items_for_test() -> list[Item]:
    test_pc = get_products_for_test()
    # [<SimpleProduct: id=1, name=item1, price=UAH 100.00>,\
    #  <SimpleProduct: id=2, name=item23, price=UAH 600.00>,\
    #  <SimpleProduct: id=3, name=item4, price=UAH 700.00>,\
    #  <SimpleProduct: id=4, name=item5, price=UAH 300.00>,\
    #  <SimpleProduct: id=6, name=item2, price=UAH 500.00>]

    items = [Item(pr=test_pc['2'], qty=3),
             Item(pr=test_pc['4'], qty=1),
             Item(pr=test_pc['6'], qty=2)]
    # [ < Item: product = < Product: id = 2, name = item23, price = UAH 600.00 >, qty = 3 >, \
    #   < Item: product = < Product: id = 4, name = item5, price = UAH 300.00 >, qty = 1 >, \
    #   < Item: product = < Product: id = 6, name = item2, price = UAH 500.00 >, qty = 2 >]
    return items
