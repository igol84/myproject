from decimal import Decimal
from typing import Union, Optional

from contracts import contract
from util.money_my import MoneyMy
from prjstore.domain.item import Item, get_items_for_test


class SaleLineItem:
    """
>>> items = get_items_for_test()                  # Create new items
>>> items                                                # get items
[<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>]
>>> sli = SaleLineItem(item=items[0], qty=2, sale_price=750)           # Create saleLineItem
>>> sli
<SaleLineItem: item=<Item: product=\
<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 750.00, qty=2>
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

    def __init__(self,
                 item: Item,
                 sale_price: Union[MoneyMy, int, float, Decimal] = None,
                 qty: int = 1,
                 currency: str = _default_curr
                 ) -> None:
        self.item: Item = item
        self.qty: int = qty
        if sale_price is None:
            self.sale_price: MoneyMy = self.item.product.price
        else:
            self.set_sale_price(sale_price, currency)

    ###############################################################################################
    # item
    def get_item(self) -> Item:
        return self._item

    @contract(pr=Item)
    def set_item(self, pr: Item) -> None:
        self._item = pr

    item = property(get_item, set_item)

    ###############################################################################################
    # qty
    def get_qty(self) -> int:
        return self._qty

    @contract(qty='int, >0')
    def set_qty(self, qty: int) -> None:
        assert self._item.qty >= qty, f'sly.qty({qty}) should not be more than item.qty({self._item.qty})!'
        self._qty = qty

    qty = property(get_qty, set_qty)

    ###############################################################################################
    # sale_price
    def get_sale_price(self) -> MoneyMy:
        return self._sale_price

    @contract(sale_price='$MoneyMy | int | float | $Decimal', currency='None | str')
    def set_sale_price(self, sale_price: Union[MoneyMy, int, float, Decimal], currency: Optional[str] = None) -> None:
        if isinstance(sale_price, MoneyMy):
            self._sale_price = sale_price
        else:
            curr = currency if currency else self._sale_price.currency
            self._sale_price = MoneyMy(amount=str(sale_price), currency=curr)

    sale_price = property(get_sale_price, set_sale_price)

    def __repr__(self):
        return f"<{self.__class__.__name__}: item={self.item}, sale_price={self.sale_price}, qty={self.qty}>"
