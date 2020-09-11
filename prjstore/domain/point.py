import datetime
from contracts import contract

from sale import Sale, Item, get_items_for_test


class Point:
    """
>>> items = get_items_for_test()
>>> items
[<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<Product: id=6, desc=item2, price=UAH 500.00>, qty=2>]
>>> point = Point('Бокс 47')
>>> point.desc = 'Магазин 2-й этаж'
>>> point.desc
'Магазин 2-й этаж'
>>> point.make_new_sale(Sale())                                          # make new empty sale
>>> point.sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')
>>> point.set_items_on_sale(items[1])                              # set items on sale
>>> point.set_items_on_sale(items[0], 2)
>>> point.unset_items_on_sale_by_pr_id('2')                                 # unset item with product id "2" from sale
>>> point.end_sale_items()
>>> point.make_new_sale()
>>> point.sale.time = datetime.datetime.strptime('11/7/20, 09:10:45', '%m/%d/%y, %H:%M:%S')
>>> point.set_items_on_sale_by_pr_id('2', 2, items)
>>> point
<Point: desc: Магазин 2-й этаж, current sale:
<Sale: time: 11/07/2020, 09:10:45, not completed, line items:
 <SaleLineItem: item=<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=2>>>
>>> point.end_sale_items()
>>> point.show_sales()
<Sale: time: 06/06/2020, 12:19:55, completed, line items:
 <SaleLineItem: item=<Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>, qty=1>
 <SaleLineItem: item=<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=1>>
<Sale: time: 11/07/2020, 09:10:45, completed, line items:
 <SaleLineItem: item=<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>, qty=2>>

    """

    def __init__(self, desc):
        self._desc = desc
        self._sales = []
        self._sale = None

    def get_desc(self) -> str:
        return self._desc

    def set_desc(self, value: str) -> None:
        self._desc = value

    desc = property(get_desc, set_desc)

    def get_sale(self) -> Sale:
        return self._sale

    sale = property(get_sale)

    @contract
    def make_new_sale(self, sale: "None | isinstance(Sale)" = None) -> None:
        if sale:
            self._sale = sale
        else:
            self._sale = Sale()

    @contract
    def set_items_on_sale(self, item: "isinstance(Item)", qty: "int, >0" = 1) -> None:
        self._sale.set_line_item(item, qty)

    @contract
    def set_items_on_sale_by_pr_id(self, pr_id: str, qty: "int, >0" = 1, items: "None | list" = None) -> None:
        self._sale.set_line_item_by_product_id(pr_id, qty, items)

    @contract
    def unset_items_on_sale_by_pr_id(self, pr_id: str, qty: "int, >0" = 1) -> None:
        self._sale.unset_line_item_by_pr_id(pr_id, qty)

    def end_sale_items(self) -> None:
        self._sale.completed()
        self._sales.append(self._sale)
        self._sale = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: desc: {self._desc}, current sale:\n{self.sale}>"

    def show_sales(self) -> None:
        sales = '\n'.join([str(sale) for sale in self._sales])
        print(sales)
