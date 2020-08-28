from contracts import contract
from product_catalog import ProductCatalog
from item import Item


class SaleLineItem:
    """
>>> test_pc=ProductCatalog().get_products_for_test() # Get test product catalog
>>> test_pc
[<Product: id=1, desc=item1, price=UAH 100.00>,\
 <Product: id=2, desc=item23, price=UAH 600.00>,\
 <Product: id=3, desc=item4, price=UAH 700.00>,\
 <Product: id=4, desc=item5, price=UAH 300.00>,\
 <Product: id=6, desc=item2, price=UAH 500.00>]
>>> items = [Item(pr=test_pc['2'], qty=3), \
             Item(pr=test_pc['4'], qty=1), \
             Item(pr=test_pc['6'], qty=2)]               # Create new items
>>> items                                                # get items
[<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<Product: id=6, desc=item2, price=UAH 500.00>, qty=2>]
>>> sli = SaleLineItem(items[0])           # Create saleLineItem
>>> sli
<SaleLineItem: item=<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=1>
>>> sli.item = items[2]                # set saleLineItem product
>>> sli.item                                            # get saleLineItem product
<Item: product=<Product: id=6, desc=item2, price=UAH 500.00>, qty=2>
>>> sli.qty = 2                                            # set saleLineItem quantity
>>> sli.qty                                                # get saleLineItem quantity
2
>>> sli
<SaleLineItem: item=<Item: product=<Product: id=6, desc=item2, price=UAH 500.00>, qty=2>, qty=2>

    """

    @contract
    def __init__(self, item: "isinstance(Item)", qty: "int" = 1) -> None:
        self._item = item
        self._qty = qty

    def __repr__(self):
        return f"<{self.__class__.__name__}: item={self._item}, qty={self._qty}>"

    def get_item(self) -> Item:
        return self._item

    @contract
    def set_item(self, pr: "isinstance(Item)") -> None:
        self._item = pr

    item = property(get_item, set_item)

    def get_qty(self) -> int:
        return self._qty

    @contract
    def set_qty(self, qty: 'int, >0') -> None:
        if self._item.qty >= qty:
            self._qty = qty
        else:
            raise ValueError(f'sly.qty({qty}) should not be more than item.qty({self._item.qty})!')

    qty = property(get_qty, set_qty)
