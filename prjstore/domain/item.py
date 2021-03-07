from contracts import contract

from prjstore.domain.product_catalog import get_products_for_test
from prjstore.domain.products import SimpleProduct, Shoes
from prjstore.domain.abstract_product import AbstractProduct

class Item:
    """
>>> test_product_catalog=get_products_for_test() # Get test product catalog
>>> test_product_catalog
[<Shoes: id=1, desc=item1, price=UAH 100.00, size=36.0>,\
 <SimpleProduct: id=2, desc=item23, price=UAH 600.00>,\
 <Shoes: id=3, desc=item4, price=UAH 700.00, size=43.3>,\
 <SimpleProduct: id=4, desc=item5, price=UAH 300.00>,\
 <SimpleProduct: id=6, desc=item2, price=UAH 500.00>]

>>> item = Item(pr=test_product_catalog['2'], qty=3)              # Create new item
>>> item                                                          # get item
<Item: product=<SimpleProduct: id=2, desc=item23, price=UAH 600.00>, qty=3>
>>> item.product                                                  # get items product
<SimpleProduct: id=2, desc=item23, price=UAH 600.00>
>>> item.product=test_product_catalog['3']                        # edit items product
>>> item.product
<Shoes: id=3, desc=item4, price=UAH 700.00, size=43.3>
>>> item.qty                                                      # get items quantity
3
>>> item.qty=2                                                    # edit items quantity
>>> item.qty
2
    """

    @contract
    def __init__(self, pr: "isinstance(AbstractProduct)", qty: 'int, >0'):
        self._product = pr
        self._qty = qty

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: product={self._product}, qty={self._qty}>'

    def get_product(self) -> AbstractProduct:
        return self._product

    @contract
    def set_product(self, pr: "isinstance(AbstractProduct)") -> None:
        self._product = pr

    product = property(get_product, set_product)

    def get_qty(self) -> int:
        return self._qty

    @contract
    def set_qty(self, qty: 'int, >0') -> None:
        self._qty = qty

    qty = property(get_qty, set_qty)


def get_items_for_test() -> list:
    test_pc = get_products_for_test()
    # [<SimpleProduct: id=1, desc=item1, price=UAH 100.00>,\
    #  <SimpleProduct: id=2, desc=item23, price=UAH 600.00>,\
    #  <SimpleProduct: id=3, desc=item4, price=UAH 700.00>,\
    #  <SimpleProduct: id=4, desc=item5, price=UAH 300.00>,\
    #  <SimpleProduct: id=6, desc=item2, price=UAH 500.00>]

    items = [Item(pr=test_pc['2'], qty=3),
             Item(pr=test_pc['4'], qty=1),
             Item(pr=test_pc['6'], qty=2)]
    # [ < Item: product = < Product: id = 2, desc = item23, price = UAH 600.00 >, qty = 3 >, \
    #   < Item: product = < Product: id = 4, desc = item5, price = UAH 300.00 >, qty = 1 >, \
    #   < Item: product = < Product: id = 6, desc = item2, price = UAH 500.00 >, qty = 2 >]
    return items
