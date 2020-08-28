from contracts import contract
from item import Item
from sale_line_item import SaleLineItem
from product_catalog import ProductCatalog
import datetime
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')


class Sale:
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
>>> sale = Sale(items[1])                                                    # Create sale
>>> sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')    # set time
>>> sale.time.strftime("%m/%d/%Y, %H:%M:%S")                                            # get time
'06/06/2020, 12:19:55'
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
<SaleLineItem: item=<Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>, qty=1>>
>>> sale.set_line_item(items[0])                                          # Add product to sale
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
<SaleLineItem: item=<Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>, qty=1>
<SaleLineItem: item=<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=1>>
>>> sale.set_line_item(items[0], 2)                                          # Add same product to sale
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
<SaleLineItem: item=<Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>, qty=1>
<SaleLineItem: item=<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=3>>
>>> sale['4']                                                    # get line item by product id "4"
<SaleLineItem: item=<Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>, qty=1>
>>> sale.completed()                                                                  # completed
>>> sale.is_complete()
True
>>> sale.not_completed()                                                              # not completed
>>> sale.is_complete()
False
>>> sale.line_items                                                                   # get sale line items
[<SaleLineItem: item=<Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>, qty=1>,\
 <SaleLineItem: item=<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=3>]



    """

    @contract
    def __init__(self, pr: "isinstance(Item)", gty: "int, >0" = 1) -> None:
        self._list_sli = []
        self._is_complete = False
        self._time = datetime.datetime.now()
        self.set_line_item(pr, gty)

    def get_list_sli(self):
        return self._list_sli

    line_items = property(get_list_sli)

    @contract
    def set_line_item(self, item: "isinstance(Item)", qty: "int, >0" = 1) -> None:  # add new line items
        if not self.is_already_set(item):  # is a new product in line items
            self._list_sli.append(SaleLineItem(item, qty))
        else:  # a same product in line items
            self[item.product.id].qty += qty

    def is_already_set(self, item) -> bool:
        return item.product in self

    def is_complete(self) -> bool:
        return self._is_complete

    def completed(self):
        self._is_complete = True

    def not_completed(self):
        self._is_complete = False

    def get_time(self) -> datetime:
        return self._time

    @contract
    def set_time(self, time) -> None:
        self._time = time

    time = property(get_time, set_time)

    def __repr__(self) -> str:
        sale_line_items = '\n' + '\n'.join([str(sli) for sli in self._list_sli])
        completed = 'completed' if self._is_complete else 'not completed'
        time = self._time.strftime("%m/%d/%Y, %H:%M:%S")
        return f"<{self.__class__.__name__}: time: {time}, {completed}, line items:{sale_line_items}>"

    def __getitem__(self, key):  # get line item by product id
        for sli in self._list_sli:
            if sli.item.product.id == key:
                return sli
        raise IndexError(f"Invalid product id: {key}")

    def __contains__(self, product):  # Does Sale contain this product in line items?
        for sli in self._list_sli:
            if product == sli.item.product:
                return True
        return False
