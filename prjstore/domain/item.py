from product_catalog import ProductCatalog, ProductDesc
from contracts import contract, new_contract

class Item():
    """
>>> test_product_catalog=ProductCatalog().get_products_for_test() # Get test product catalog
>>> test_product_catalog
{'1': <Product: id=1, desc=item1, price=UAH 100.00>, '6': <Product: id=6, desc=item2, price=UAH 500.00>, \
'2': <Product: id=2, desc=item23, price=UAH 600.00>, '3': <Product: id=3, desc=item4, price=UAH 700.00>, \
'4': <Product: id=4, desc=item5, price=UAH 300.00>}
>>> item = Item(pc=test_product_catalog['2'], qty=3)              # Create new item
>>> item                                                          # get item
<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>
>>> item.product                                                  # get items product
<Product: id=2, desc=item23, price=UAH 600.00>
>>> item.product=test_product_catalog['3']                        # edit items product
>>> item.product
<Product: id=3, desc=item4, price=UAH 700.00>
>>> item.qty                                                      # get items quantity
3
>>> item.qty=2                                                    # edit items quantity
>>> item.qty
2
    """
    @contract()
    def __init__(self, pc: "isinstance(ProductDesc)", qty: 'int, >0'):
        self._product = pc
        self._qty = qty

    def __repr__(self):
        return f'<{self.__class__.__name__}: product={self._product}, qty={self._qty}>'

    def get_product(self):
        return self._product

    @contract
    def set_product(self, pc: "isinstance(ProductDesc)"):
        self._product = pc

    product = property(get_product, set_product)

    def get_qty(self):
        return self._qty

    @contract
    def set_qty(self, qty: 'int, >0'):
        self._qty = qty

    qty = property(get_qty, set_qty)
