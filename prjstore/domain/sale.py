from contracts import contract
import datetime
import locale

from prjstore.domain.item import Item, get_items_for_test
from prjstore.domain.sale_line_item import SaleLineItem
from prjstore.domain.product_catalog import SimpleProduct

locale.setlocale(locale.LC_TIME, 'ru_RU')


class Sale:
    """
>>> items = get_items_for_test()                                               # get items
>>> items
[<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>]
>>> sale = Sale(items[1])                                                    # Create sale
>>> sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')    # set time
>>> sale.time.strftime("%m/%d/%Y, %H:%M:%S")                                            # get time
'06/06/2020, 12:19:55'
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, qty=1>>
>>> sale.set_line_item(items[0])                                          # Add product to sale
>>> sale.set_line_item(items[2])
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, qty=1>
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, qty=1>
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, qty=1>>
>>> sale.set_line_item(items[0], 2)                                          # Add same product to sale
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, qty=1>
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, qty=3>
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, qty=1>>
>>> sale['4']                                                    # get line item by product id "4"
<SaleLineItem: item=<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, qty=1>
>>> sale.completed()                                                                  # completed
>>> sale.is_complete()
True
>>> sale.not_completed()                                                              # not completed
>>> sale.is_complete()
False
>>> sale.unset_line_item_by_pr_id('2', 2)                                 # unset sale line pr id ='2'# items 3-2=1
>>> sale.line_items                                                                   # get sale line items
[<SaleLineItem: item=<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, qty=1>,\
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, qty=1>,\
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, qty=1>]

>>> del sale['4']                                                             # del sale line item by product id='4'
>>> sale.line_items
[<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, qty=1>,\
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, qty=1>]
>>> sale.unset_line_item_by_pr_id('6')                           # unset sale line pr id ='6' items 1-1=0 -> del
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, qty=1>>
>>> sale.set_line_item_by_product_id('2',items,2)        # set sale line pr id ='2' items 1+2=3 -> del
>>> sale.set_line_item_by_product_id('6',items,2)
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, qty=3>
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, qty=2>>

    """

    @contract
    def __init__(self, item: "None | isinstance(Item)" = None, gty: "None | int, >0" = 1) -> None:
        self._list_sli = []
        self._is_complete = False
        self._time = datetime.datetime.now()
        if item:
            self.set_line_item(item, gty)

    def get_list_sli(self):
        return self._list_sli

    line_items = property(get_list_sli)

    @contract(item=Item, qty="int, >0")
    def set_line_item(self, item, qty=1) -> None:  # add new line items
        if not self.is_item_already_set(item):  # is a new product in line items
            self._list_sli.append(SaleLineItem(item, qty))
        else:  # a same product in line items
            self[item.product.id].qty += qty

    @contract(pr_id=str, qty='int, >0', items='None | list')
    def set_line_item_by_product_id(self, pr_id, items=None, qty=1) -> None:  # add new line items by product id
        try:
            if self.get_line_item_by_product_id(pr_id):  # try to get line items by product id
                self[pr_id].qty += qty
        except IndexError:  # is a new product in line items, must use items list
            if items:
                for item in items:
                    if isinstance(item, Item) and item.product.id == pr_id:
                        self.set_line_item(item, qty)
                        return None
            raise IndexError(f"Invalid product id: {pr_id}")

    @contract(item=Item)
    def is_item_already_set(self, item) -> bool:
        return item.product in self

    @contract(pr_id=str)
    def get_line_item_by_product_id(self, pr_id) -> SaleLineItem:
        for sli in self._list_sli:
            if sli.item.product.id == pr_id:
                return sli
        raise IndexError(f"Invalid product id: {pr_id}")

    @contract(pr_id=str, qty='int, >0')
    def unset_line_item_by_pr_id(self, pr_id, qty=1) -> None:  # unset line items
        sli = self.get_line_item_by_product_id(pr_id)
        assert sli and qty <= sli.qty, f"quantity({qty}) should not be more than item.qty({self[pr_id].qty})!"
        # a same product in line items
        if qty < sli.qty:
            self[pr_id].qty -= qty
        elif qty == sli.qty:
            del self[pr_id]

    @contract(pr_id=str)
    def del_line_item_by_product_id(self, pr_id) -> None:
        for key, sli in enumerate(self._list_sli):
            if sli.item.product.id == pr_id:
                del self._list_sli[key]

    def is_complete(self) -> bool:
        return self._is_complete

    def completed(self) -> bool:
        self._is_complete = True

    def not_completed(self) -> bool:
        self._is_complete = False

    def get_time(self) -> datetime:
        return self._time

    @contract(time=datetime.datetime)
    def set_time(self, time) -> None:
        self._time = time

    time = property(get_time, set_time)

    @contract(product=SimpleProduct)
    def is_product_in_sale(self, product) -> bool:
        for sli in self._list_sli:
            if product == sli.item.product:
                return True
        return False

    def __repr__(self) -> str:
        sale_line_items = '\n ' + '\n '.join([str(sli) for sli in self._list_sli])
        completed = 'completed' if self._is_complete else 'not completed'
        time = self._time.strftime("%m/%d/%Y, %H:%M:%S")
        return f"<{self.__class__.__name__}: time: {time}, {completed}, line items:{sale_line_items}>"

    def __getitem__(self, key):  # get line item by product id
        return self.get_line_item_by_product_id(key)

    def __delitem__(self, key):  # del sale line item by product id
        self.del_line_item_by_product_id(key)

    def __contains__(self, product) -> bool:  # Does Sale contain this product in line items?
        return self.is_product_in_sale(product)
