from contracts import contract

from prjstore.domain.item import Item, get_items_for_test


class SaleLineItem:
    """
>>> items = get_items_for_test()                  # Create new items
>>> items                                                # get items
[<Item: product=<SimpleProduct: id=2, desc=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<SimpleProduct: id=4, desc=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<SimpleProduct: id=6, desc=item2, price=UAH 500.00>, qty=2>]
>>> sli = SaleLineItem(items[0])           # Create saleLineItem
>>> sli
<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=1>
>>> sli.item = items[2]                # set saleLineItem product
>>> sli.item                                            # get saleLineItem product
<Item: product=<SimpleProduct: id=6, desc=item2, price=UAH 500.00>, qty=2>
>>> sli.qty = 2                                            # set saleLineItem quantity
>>> sli.qty                                                # get saleLineItem quantity
2
>>> sli
<SaleLineItem: item=<Item: product=<SimpleProduct: id=6, desc=item2, price=UAH 500.00>, qty=2>, qty=2>

    """

    @contract(item=Item, qty=int)
    def __init__(self, item, qty=1) -> None:
        self._item = item
        self._qty = qty

    def __repr__(self):
        return f"<{self.__class__.__name__}: item={self._item}, qty={self._qty}>"

    def get_item(self) -> Item:
        return self._item

    @contract(pr=Item)
    def set_item(self, pr) -> None:
        self._item = pr

    item = property(get_item, set_item)

    def get_qty(self) -> int:
        return self._qty

    @contract(qty='int, >0')
    def set_qty(self, qty) -> None:
        assert self._item.qty >= qty, f'sly.qty({qty}) should not be more than item.qty({self._item.qty})!'
        self._qty = qty

    qty = property(get_qty, set_qty)
