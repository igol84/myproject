from dataclasses import field
from decimal import Decimal
from typing import overload
from datetime import datetime
import locale

from pydantic import conint, validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.domain.item import Item
from prjstore.domain.sale_line_item import SaleLineItem
from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.seller import Seller
from util.money import Money

locale.setlocale(locale.LC_TIME, 'ru_RU')


@dataclass
class Sale:
    seller: Seller = None
    list_sli: list[SaleLineItem] = field(default_factory=list)
    date_time: datetime = datetime.now()
    complete: bool = False

    ###############################################################################################
    # add new line items
    @validate_arguments
    def add_line_item(self, item: Item, sale_price: float = None, qty: conint(ge=0) = 1) -> None:
        sale_price = sale_price if sale_price is not None else item.product.price.amount
        assert qty <= item.qty, f"qty({qty}) should not be more than item.qty({item.qty})!"
        # a same product in line items
        if self[item.id, sale_price]:
            self[item.id, sale_price].qty += qty
        # is a new product in line items
        else:
            self.list_sli.append(SaleLineItem(item=item, sale_price=(sale_price,), qty=qty))
        item.qty -= qty

    @validate_arguments
    def get_line_items_by_product_id(self, pr_id: str) -> list[SaleLineItem]:
        list_sli = []
        for sli in self.list_sli:
            if sli.item.product.prod_id == pr_id:
                list_sli.append(sli)
        return list_sli

    @validate_arguments
    def get_line_items_by_product_id_and_sale_price(self, pr_id: str, sale_price: float) -> list[SaleLineItem]:
        list_sli = []
        for sli in self.list_sli:
            if sli.item.product.prod_id == pr_id and sli.sale_price.amount == sale_price:
                list_sli.append(sli)
        return list_sli

    @validate_arguments
    def get_line_items_by_item_id(self, item_id: int) -> list[SaleLineItem]:
        list_sli = []
        for sli in self.list_sli:
            if sli.item.id == item_id:
                list_sli.append(sli)
        return list_sli

    @validate_arguments
    def get_line_item_by_item_id_and_sale_price(self, item_id: int, sale_price: float) -> SaleLineItem:
        for sli in self.list_sli:
            if sli.item.id == item_id and sli.sale_price.amount == sale_price:
                return sli

    @validate_arguments
    def edit_sale_price(self, sli: SaleLineItem, sale_price: float):
        old_same_sli = self.get_line_item_by_item_id_and_sale_price(sli.item.id, sale_price)
        if old_same_sli:
            self.list_sli.remove(sli)
            old_same_sli.qty += sli.qty
        else:
            sli.sale_price.amount = sale_price

    # unset line items
    @validate_arguments
    def unset_line_item(self, sli: SaleLineItem, qty: int = 1) -> None:
        sale_price = sli.sale_price.amount
        assert sli and qty <= sli.qty, f"qty({qty}) should not be more " \
                                       f"than item.qty({self[(sli.item.id, sale_price)].qty})!"
        if qty < sli.qty:
            self[(sli.item.id, sale_price)].qty -= qty
        elif qty == sli.qty:
            del self[(sli.item.id, sale_price)]

    @validate_arguments
    def unset_line_items_by_pr_id_and_sale_price(self, pr_id: str, sale_price: float, qty: int = 1) -> None:
        list_sli = self.get_line_items_by_product_id_and_sale_price(pr_id, sale_price)
        for sli in list_sli:
            self.unset_line_item(sli, qty)

    @validate_arguments
    def del_line_items_by_product_id_and_sale_price(self, pr_id: str, sale_price: float) -> None:
        for key, sli in enumerate(self.list_sli):
            if sli.item.product.prod_id == pr_id and sli.sale_price.amount == sale_price:
                del self.list_sli[key]

    @validate_arguments
    def del_line_items_by_item_id_and_sale_price(self, item_id: int, sale_price: float) -> None:
        for key, sli in enumerate(self.list_sli):
            if sli.item.id == item_id and sli.sale_price.amount == sale_price:
                del self.list_sli[key]

    def is_complete(self) -> bool:
        return self.complete

    def completed(self) -> None:
        self.complete = True

    @validate_arguments
    def is_item_in_sale(self, item: Item) -> bool:
        return item.product in self

    @validate_arguments
    def is_product_in_sale(self, product: AbstractProduct, sale_price: float = None) -> bool:
        for sli in self.list_sli:
            if sale_price:
                if sli.item.product == product and sli.sale_price.amount == sale_price:
                    return True
            else:
                if product == sli.item.product:
                    return True
        return False

    def get_total(self) -> Money:
        total = Money(0)
        for sli in self.list_sli:
            total += sli.sale_price * sli.qty
        return total

    def get_total_purchase(self) -> Money:
        total = Money(0)
        for sli in self.list_sli:
            total += sli.item.buy_price * sli.qty
        return total

    def get_total_profit(self) -> Money:
        return self.get_total() - self.get_total_purchase()

    @overload
    def __getitem__(self, key: int) -> list[SaleLineItem]:
        ...

    @overload
    def __getitem__(self, key: tuple[int, float]) -> SaleLineItem:
        ...

    def __getitem__(self, key) -> list[SaleLineItem]:  # get line item by product id
        if isinstance(key, int):
            item_id = key
            return self.get_line_items_by_item_id(item_id)
        elif isinstance(key, tuple) and isinstance(key[0], int) and \
                (isinstance(key[1], int) or isinstance(key[1], float) or isinstance(key[1], Decimal)):
            item_id, sale_price = key
            return self.get_line_item_by_item_id_and_sale_price(item_id, sale_price)
        else:
            raise ValueError('invalid key', key)

    def __delitem__(self, key: tuple[int, float]):  # del sale line item by product id
        item_id, sale_price = key
        self.del_line_items_by_item_id_and_sale_price(item_id, sale_price)

    def __contains__(self, product: AbstractProduct) -> bool:  # Does Sale contain this product in line items?
        return self.is_product_in_sale(product)

    def __len__(self):
        return len(self.list_sli)
