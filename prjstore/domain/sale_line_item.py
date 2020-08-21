from contracts import contract
from product_catalog import ProductDesc, ProductCatalog


class SaleLineItem:
    '''
>>> test_product_catalog=ProductCatalog().get_products_for_test() # Get test product catalog
>>> test_product_catalog
{'1': <Product: id=1, desc=item1, price=UAH 100.00>, '6': <Product: id=6, desc=item2, price=UAH 500.00>, \
'2': <Product: id=2, desc=item23, price=UAH 600.00>, '3': <Product: id=3, desc=item4, price=UAH 700.00>, \
'4': <Product: id=4, desc=item5, price=UAH 300.00>}
>>> sli = SaleLineItem(test_product_catalog['1'])                                 # Create saleLineItem
>>> sli
<SaleLineItem: product=<Product: id=1, desc=item1, price=UAH 100.00>, qty=1>
>>> sli.product = test_product_catalog['3']                # set saleLineItem product
>>> sli.product                                            # get saleLineItem product
<Product: id=3, desc=item4, price=UAH 700.00>
>>> sli.qty = 3                                            # set saleLineItem quantity
>>> sli.qty                                                # get saleLineItem quantity
3
>>> sli
<SaleLineItem: product=<Product: id=3, desc=item4, price=UAH 700.00>, qty=3>

    '''

    @contract
    def __init__(self, pd: "isinstance(ProductDesc)", qty: "int"=1) -> None:
        self._product = pd
        self._qty = qty

    def __repr__(self):
        return f"<{self.__class__.__name__}: product={self._product}, qty={self._qty}>"

    def get_product(self) -> ProductDesc:
        return self._product

    @contract
    def set_product(self, pr: "isinstance(ProductDesc)") -> None:
        self._product = pr

    product = property(get_product, set_product)

    def get_qty(self) -> int:
        return self._qty

    @contract
    def set_qty(self, qty: 'int, >0') -> None:
        self._qty = qty

    qty = property(get_qty, set_qty)