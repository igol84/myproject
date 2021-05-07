from contracts import contract
from util.money_my import MoneyMy
from .item import Item, get_items_for_test


class SaleLineItem:
    """
>>> items = get_items_for_test()                  # Create new items
>>> items                                                # get items
[<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>]
>>> sli = SaleLineItem(items[0])           # Create saleLineItem
>>> sli
<SaleLineItem: item=<Item: product=\
<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=1>
>>> sli.item = items[2]                # set saleLineItem product
>>> sli.item                                            # get saleLineItem product
<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>
>>> sli.qty = 2                                            # set saleLineItem quantity
>>> sli.qty                                                # get saleLineItem quantity
2
>>> sli.sale_price = 500
>>> print(sli.sale_price)
UAH 500.00
>>> sli
<SaleLineItem: item=<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, sale_price=UAH 500.00, \
qty=2>

    """
    _default_curr = MoneyMy.default_currency

    def __init__(self, item, qty=1, sale_price=None, currency=_default_curr) -> None:
        self.item = item
        self.qty = qty
        if sale_price is None:
            self.sale_price = self.item.product.price
        else:
            self.set_sale_price(sale_price, currency)

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

    def get_sale_price(self) -> MoneyMy:
        return self._sale_price

    def set_sale_price(self, sale_price, currency=None) -> None:
        if isinstance(sale_price, MoneyMy):
            self._sale_price = sale_price
        else:
            curr = currency if currency else self._sale_price.currency
            self._sale_price = MoneyMy(amount=str(sale_price), currency=curr)

    sale_price = property(get_sale_price, set_sale_price)

    def __repr__(self):
        return f"<{self.__class__.__name__}: item={self.item}, sale_price={self.sale_price}, qty={self.qty}>"
