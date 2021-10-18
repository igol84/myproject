import datetime
import collections
from typing import Optional

from pydantic import validate_arguments

from prjstore.db import API_DB
from prjstore.domain.store import Store
from prjstore.domain.item import Item
from prjstore.domain.sale import Sale
from prjstore.domain.test.test_item import TestItem
from prjstore.domain.test.test_place_of_sale import TestPlaceOfSale
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from prjstore.domain.test.test_seller import TestSeller
from prjstore.ui.schemas.sale_registration import ViewItem
from util.money import Money


class SaleRegistrationHandler:
    def __init__(self, db=API_DB(), test=False):
        self.db = db
        self._store = Store.create_from_schema(self.db.store.get(id=1))
        self._sale = Sale()
        if test:
            self._test()

    def _test(self):
        test = TestProductCatalog()
        test.setUp()
        self._store.pc = test.pc
        test = TestItem()
        test.setUp()
        self._store.items = test.items
        test = TestSeller()
        test.setUp()
        self._store.sellers = test.sellers
        test = TestPlaceOfSale()
        test.setUp(sale=False)
        self._store.places_of_sale = test.places_of_sale
        self._store.places_of_sale[1].sale = None
        self._store.items[1].qty = 150
        self._store.items[1].product.price = Money(10500)
        self._store.items[1].product.name = 'Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!'

    @validate_arguments
    def get_store_items(self, search: Optional[str] = None) -> dict[str, ViewItem]:
        items: dict[int: Item] = self._store.items if not search else self.search_items(search)
        items = collections.OrderedDict(sorted(items.items()))
        products: dict[str: ViewItem] = {}
        for item_ in items.values():
            if item_.product.prod_id not in products:
                products[item_.product.prod_id] = ViewItem(
                    prod_id=item_.product.prod_id,
                    name=item_.product.name,
                    price=item_.product.price.amount,
                    price_format=item_.product.price.format(),
                    qty=item_.qty
                )
            else:
                products[item_.product.prod_id].qty += item_.qty
        return products

    @validate_arguments
    def get_sale_line_items(self) -> dict[tuple[str, float]: ViewItem]:
        products: dict[tuple[str, float]: ViewItem] = {}
        for sli in self._sale.list_sli:
            if (sli.item.product.prod_id, sli.sale_price.amount) not in products:
                products[sli.item.product.prod_id, sli.sale_price.amount] = ViewItem(
                    prod_id=sli.item.product.prod_id,
                    name=sli.item.product.name,
                    price=sli.sale_price.amount,
                    price_format=sli.sale_price.format(),
                    qty=sli.qty
                )
            else:
                products[sli.item.product.prod_id, sli.sale_price.amount].qty += sli.qty
        return products

    @validate_arguments
    def search_items(self, text: str) -> dict[str: Item]:
        items = self._store.search_items_by_name(name=text)
        if text in self._store.items:  # search_items_by_id
            items[text] = self._store.items[text]
        return items

    @validate_arguments
    def put_on_sale(self, pr_id: str, qty: int, sale_price: float = None) -> None:
        sale_items = self._store.get_items_by_pr_id(pr_id)
        qty_need_to_add = qty
        for sale_item in sale_items:
            qty_line_item = sale_item.qty if qty_need_to_add > sale_item.qty else qty_need_to_add
            self._sale.add_line_item(item=sale_item, qty=qty_line_item, sale_price=sale_price)
            if sale_item.qty == 0:
                del self._store.items[sale_item.id]
            qty_need_to_add -= qty_line_item
            if qty_need_to_add == 0:
                break

    @validate_arguments
    def is_item_exists(self, pr_id: str) -> bool:
        return pr_id in self._store.items

    @validate_arguments
    def get_item_qty_by_product_id(self, pr_id: str) -> int:
        if pr_id in self._store.items:
            return self._store.items[pr_id].qty

    @validate_arguments
    def put_item_form_sli_to_items(self, pr_id: str, sli_price: float) -> None:
        sli_s = self._sale.get_line_items_by_product_id_and_sale_price(pr_id, sli_price)
        for sli in sli_s:
            self._sale.unset_line_item(sli=sli, qty=sli.qty)
            self._store.add_item(item=sli.item, qty=sli.qty)

    @validate_arguments
    def edit_sale_price_in_sli(self, sli_product_id: str, old_sale_price: float, sale_price: float) -> None:
        sli_s = self._sale.get_line_items_by_product_id_and_sale_price(sli_product_id, old_sale_price)
        for sli in sli_s:
            self._sale.edit_sale_price(sli, sale_price)

    def get_store_places_of_sale_names(self) -> dict[int, str]:
        return {sale_id: place_of_sale.name for sale_id, place_of_sale in list(self._store.places_of_sale.items())}

    def get_store_sellers_names(self) -> dict[int, str]:
        return {seller_id: seller.name for seller_id, seller in list(self._store.sellers.items())}

    def get_total(self) -> str:
        total_str = ''
        if self._sale.list_sli:
            total = self._sale.get_total()
            total_purchase = self._sale.get_total_profit()
            total_str = f'Выручка: {total.format()}; Прибыль: {total_purchase.format()}'
        return total_str

    @validate_arguments
    def end_sale(self, date: datetime.date, current_place_of_sale_id: Optional[int],
                 current_seller_id: Optional[int]) -> bool:
        if current_place_of_sale_id is not None and current_seller_id is not None and self._sale.list_sli:
            time = datetime.datetime.min.time()
            self._sale.date_time = datetime.datetime.combine(date, time)
            self._sale.seller = self._store.sellers[current_seller_id]
            current_place = self._store.places_of_sale[current_place_of_sale_id]
            current_place.sale = self._sale
            self._sale.completed()
            pd_sale = self._sale.schema_create(place_id=current_place_of_sale_id)
            if sale:=self.db.sale.create(pd_sale):
                return sale
        return False


if __name__ == '__main__':
    handler = SaleRegistrationHandler(test=True)

    for key, item in sorted(handler.get_store_items().items()):
        print(key, item)
