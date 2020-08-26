from contracts import contract
from sale_line_item import SaleLineItem
from product_catalog import ProductCatalog, ProductDesc
import datetime
import locale

locale.setlocale(locale.LC_TIME, 'ru_RU')


class Sale:
    '''
>>> test_pc=ProductCatalog().get_products_for_test()                            # Get test product catalog
>>> test_pc                                                                     # get catalog
{'1': <Product: id=1, desc=item1, price=UAH 100.00>, '6': <Product: id=6, desc=item2, price=UAH 500.00>,\
 '2': <Product: id=2, desc=item23, price=UAH 600.00>, '3': <Product: id=3, desc=item4, price=UAH 700.00>,\
 '4': <Product: id=4, desc=item5, price=UAH 300.00>}

>>> sale = Sale(test_pc['1'])                                                    # Create sale
>>> sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')    # set time
>>> sale.time.strftime("%m/%d/%Y, %H:%M:%S")                                            # get time
'06/06/2020, 12:19:55'
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
<SaleLineItem: product=<Product: id=1, desc=item1, price=UAH 100.00>, qty=1>>
>>> sale.set_line_item(test_pc['3'], 3)                                          # Add product to sale
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
<SaleLineItem: product=<Product: id=1, desc=item1, price=UAH 100.00>, qty=1>
<SaleLineItem: product=<Product: id=3, desc=item4, price=UAH 700.00>, qty=3>>
>>> sale.set_line_item(test_pc['1'], 3)                                          # Add same product to sale
>>> sale
<Sale: time: 06/06/2020, 12:19:55, not completed, line items:
<SaleLineItem: product=<Product: id=1, desc=item1, price=UAH 100.00>, qty=4>
<SaleLineItem: product=<Product: id=3, desc=item4, price=UAH 700.00>, qty=3>>
>>> sale.complete                                                                # is complete?
False
>>> sale.complete = True                                                         # complete
>>> sale.line_items                                                         # get sale line items
{'1': <SaleLineItem: product=<Product: id=1, desc=item1, price=UAH 100.00>, qty=4>,\
 '3': <SaleLineItem: product=<Product: id=3, desc=item4, price=UAH 700.00>, qty=3>}


    '''

    @contract
    def __init__(self, pr: "isinstance(ProductDesc)", gty: "int, >0" = 1) -> None:
        self._list_sli = dict()
        self._is_complete = False
        self._time = datetime.datetime.now()
        self.set_line_item(pr, gty)

    def get_list_sli(self):
        return self._list_sli

    line_items = property(get_list_sli)

    @contract
    def set_line_item(self, pr: "isinstance(ProductDesc)", qty: "int, >0" = 1) -> None:
        if not self.is_already_set(pr):
            self._list_sli[pr.id] = SaleLineItem(pr, qty)
        else:
            self._list_sli[pr.id].qty += qty

    def is_complete(self) -> bool:
        return self._is_complete

    @contract
    def change_complete(self, val: "bool") -> None:
        self._is_complete = val

    complete = property(is_complete, change_complete)

    def is_already_set(self, pr) -> bool:
        return pr.id in self._list_sli

    def get_time(self) -> datetime:
        return self._time

    @contract
    def set_time(self, time) -> None:
        self._time = time

    time = property(get_time, set_time)

    def __repr__(self) -> str:
        sale_line_items = '\n' + '\n'.join([str(sli) for id, sli in self._list_sli.items()])
        completed = 'completed' if self._is_complete else 'not completed'
        time = self._time.strftime("%m/%d/%Y, %H:%M:%S")
        return f"<{self.__class__.__name__}: time: {time}, {completed}, line items:{sale_line_items}>"
