from typing import Optional

from contracts import contract
from datetime import datetime
import locale

from prjstore.domain.item import Item, get_items_for_test
from prjstore.domain.sale_line_item import SaleLineItem
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.seller import Seller

locale.setlocale(locale.LC_TIME, 'ru_RU')


class Sale:
    """
>>> items: list[Item] = get_items_for_test()                                               # get items
>>> items
[<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>]
>>> sale = Sale(Seller('Igor'), items[1])                                                    # Create sale
>>> sale.time = datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')    # set time
>>> sale.time.strftime("%m/%d/%Y, %H:%M:%S")                                            # get time
'06/06/2020, 12:19:55'
>>> sale
<Sale: seller:Igor, time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, sale_price=UAH 300.00, qty=1>>

>>> sale.seller = Seller('Anna')
>>> sale.seller.name
'Anna'

>>> sale.add_line_item(items[0])                                          # Add product to sale
>>> sale.add_line_item(items[2])
>>> sale
<Sale: seller:Anna, time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, sale_price=UAH 300.00, qty=1>
 <SaleLineItem: item=\
<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=1>
 <SaleLineItem: item=\
<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, sale_price=UAH 500.00, qty=1>>
>>> sale.add_line_item(items[0], 2)                                          # Add same product to sale
>>> sale
<Sale: seller:Anna, time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, sale_price=UAH 300.00, qty=1>
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=3>
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, sale_price=UAH 500.00, qty=1>>
>>> sale['4']                                                    # get line item by product id "4"
<SaleLineItem: item=<Item: product=\
<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, sale_price=UAH 300.00, qty=1>
>>> sale.unset_line_item_by_pr_id('2', 2)                                 # unset sale line pr id ='2'# items 3-2=1
>>> sale.line_items                                                                   # get sale line items
[<SaleLineItem: item=<Item: product=\
<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, sale_price=UAH 300.00, qty=1>,\
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=1>,\
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, sale_price=UAH 500.00, qty=1>]

>>> del sale['4']                                                             # del sale line item by product id='4'
>>> sale.line_items
[<SaleLineItem: item=<Item: product=\
<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=1>,\
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, sale_price=UAH 500.00, qty=1>]
>>> sale.unset_line_item_by_pr_id('6')                           # unset sale line pr id ='6' items 1-1=0 -> del
>>> sale
<Sale: seller:Anna, time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=1>>
>>> sale.add_line_item_by_product_id('2',items,2)        # set sale line pr id ='2' items 1+2=3 -> del
>>> sale.add_line_item_by_product_id('6',items,2)
>>> sale
<Sale: seller:Anna, time: 06/06/2020, 12:19:55, not completed, line items:
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=3>
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, sale_price=UAH 500.00, qty=2>>
>>> sale.completed()                                                                  # completed
>>> sale.is_complete()
True
>>> sale
<Sale: seller:Anna, time: 06/06/2020, 12:19:55, completed, line items:
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=3>
 <SaleLineItem: item=<Item: product=\
<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>, sale_price=UAH 500.00, qty=2>>
    """

    def __init__(self, seller: Seller = None, item: Item = None, gty: int = 1) -> None:
        self.seller: Seller = seller
        self.__list_sli: list[SaleLineItem] = []
        self.__is_complete: bool = False
        self.time: datetime = datetime.now()

        if item:
            self.add_line_item(item, gty)

    ###############################################################################################
    # seller
    def get_seller(self) -> Seller:
        return self.__seller

    @contract(seller='None | $Seller')
    def set_seller(self, seller: Optional[Seller]) -> None:
        self.__seller = seller

    seller = property(get_seller, set_seller)

    ###############################################################################################
    # line_items
    def get_list_sli(self) -> list[SaleLineItem]:
        return self.__list_sli

    line_items = property(get_list_sli)

    ###############################################################################################
    # time
    def get_time(self) -> datetime:
        return self.__time

    @contract(time=datetime)
    def set_time(self, time: datetime) -> None:
        self.__time = time

    time = property(get_time, set_time)

    ###############################################################################################
    # add new line items
    @contract(item=Item, qty="int, >0")
    def add_line_item(self, item: Item, qty: int = 1) -> None:
        if not self.is_item_in_sale(item):  # is a new product in line items
            self.__list_sli.append(SaleLineItem(item, qty))
        else:  # a same product in line items
            self[item.product.id].qty += qty

    # add new line items by product id
    @contract(pr_id=str, items='None | list', qty='int, >0')
    def add_line_item_by_product_id(self, pr_id: str, items: list[Item] = None, qty: int = 1) -> None:
        try:
            if self.get_line_item_by_product_id(pr_id):  # try to get line items by product id
                self[pr_id].qty += qty
        except IndexError:  # is a new product in line items, must use items list
            if items:
                for item in items:
                    if isinstance(item, Item) and item.product.id == pr_id:
                        self.add_line_item(item, qty)
                        return None
            raise IndexError(f"Invalid product id: {pr_id}")

    @contract(pr_id=str)
    def get_line_item_by_product_id(self, pr_id: str) -> SaleLineItem:
        for sli in self.__list_sli:
            if sli.item.product.id == pr_id:
                return sli
        raise IndexError(f"Invalid product id: {pr_id}")

    @contract(pr_id=str, qty='int, >0')
    def unset_line_item_by_pr_id(self, pr_id: str, qty: int = 1) -> None:  # unset line items
        sli = self.get_line_item_by_product_id(pr_id)
        assert sli and qty <= sli.qty, f"quantity({qty}) should not be more than item.qty({self[pr_id].qty})!"
        # a same product in line items
        if qty < sli.qty:
            self[pr_id].qty -= qty
        elif qty == sli.qty:
            del self[pr_id]

    @contract(pr_id=str)
    def del_line_item_by_product_id(self, pr_id: str) -> None:
        for key, sli in enumerate(self.__list_sli):
            if sli.item.product.id == pr_id:
                del self.__list_sli[key]

    def is_complete(self) -> bool:
        return self.__is_complete

    def completed(self) -> None:
        self.__is_complete = True

    @contract(item=Item)
    def is_item_in_sale(self, item: Item) -> bool:
        return item.product in self

    @contract(product=AbstractProduct)
    def is_product_in_sale(self, product: AbstractProduct) -> bool:
        for sli in self.__list_sli:
            if product == sli.item.product:
                return True
        return False

    def __repr__(self) -> str:
        sale_line_items = '\n ' + '\n '.join([str(sli) for sli in self.line_items])
        completed = 'completed' if self.is_complete() else 'not completed'
        time = self.time.strftime("%m/%d/%Y, %H:%M:%S")
        return f"<{self.__class__.__name__}: " \
               f"seller:{self.seller.name}, time: {time}, {completed}, line items:{sale_line_items}>"

    def __getitem__(self, key: str):  # get line item by product id
        return self.get_line_item_by_product_id(key)

    def __delitem__(self, key: str):  # del sale line item by product id
        self.del_line_item_by_product_id(key)

    def __contains__(self, product: AbstractProduct) -> bool:  # Does Sale contain this product in line items?
        return self.is_product_in_sale(product)

    def __len__(self):
        return len(self.line_items)
