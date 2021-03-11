import datetime
from contracts import contract

from prjstore.domain.sale import Sale, Item, get_items_for_test


class PlaceOfSale:
    """
>>> items = get_items_for_test()
>>> items
[<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>]
>>> PlaceOfSale = PlaceOfSale('Бокс 47')
>>> PlaceOfSale.name = 'Магазин 2-й этаж'
>>> PlaceOfSale.name
'Магазин 2-й этаж'
>>> PlaceOfSale.make_new_sale(Sale())                                          # make new empty sale
>>> PlaceOfSale.sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')
>>> PlaceOfSale.set_items_on_sale(items[1])                              # set items on sale
>>> PlaceOfSale.set_items_on_sale(items[0], 2)
>>> PlaceOfSale.unset_items_on_sale_by_pr_id('2')                                 # unset item with product id "2" from sale
>>> PlaceOfSale.end_sale_items()
>>> PlaceOfSale.make_new_sale()
>>> PlaceOfSale.sale.time = datetime.datetime.strptime('11/7/20, 09:10:45', '%m/%d/%y, %H:%M:%S')
>>> PlaceOfSale.set_items_on_sale_by_pr_id('2', 2, items)
>>> PlaceOfSale
<PlaceOfSale: name: Магазин 2-й этаж, current sale:
<Sale: time: 11/07/2020, 09:10:45, not completed, line items:
 <SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=2>>>
>>> PlaceOfSale.end_sale_items()


    """

    def __init__(self, name):
        self.name = name
        self._sale = None

    def get_name(self) -> str:
        return self._name

    def set_name(self, value: str) -> None:
        self._name = value

    name = property(get_name, set_name)

    def get_sale(self) -> Sale:
        return self._sale

    @contract(sale=Sale)
    def set_sale(self, sale) -> None:
        self._sale = sale

    def del_sale(self) -> None:
        self._sale = None

    sale = property(get_sale, set_sale, del_sale)

    @contract(sale="None | $Sale")
    def make_new_sale(self, sale=None) -> None:
        if sale:
            self.sale = sale
        else:
            self.sale = Sale()

    @contract(item=Item, qty="int, >0")
    def set_items_on_sale(self, item, qty=1) -> None:
        self.sale.add_line_item(item, qty)

    @contract(pr_id=str, qty="int, >0", items="None | list")
    def set_items_on_sale_by_pr_id(self, pr_id, qty=1, items=None) -> None:
        self.sale.add_line_item_by_product_id(pr_id, items, qty)

    @contract(pr_id=str, qty="int, >0")
    def unset_items_on_sale_by_pr_id(self, pr_id, qty=1) -> None:
        self.sale.unset_line_item_by_pr_id(pr_id, qty)

    def end_sale_items(self) -> None:
        if self.sale:
            self.sale.completed()
            del self.sale

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: name: {self._name}, current sale:\n{self.sale}>"
