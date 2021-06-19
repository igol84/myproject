import datetime
from typing import Union, Optional

from pydantic import validate_arguments

from prjstore.domain.item import Item
from prjstore.domain.sale import Sale
from prjstore.domain.store import Store
from prjstore.domain.test.test_item import TestItem
from prjstore.domain.test.test_place_of_sale import TestPlaceOfSale
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from prjstore.domain.test.test_seller import TestSeller
from util.money import Money


class SaleRegistrationHandler:
    def __init__(self, test=False):
        self._store = Store()
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
        self._store.places_of_sale[0].sale = None
        self._store.items['1'].qty = 150
        self._store.items['1'].product.price = Money(10500)
        self._store.items['1'].product.name = 'Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!'

    @validate_arguments
    def get_store_items(self, search: Optional[str] = None) -> dict[str: dict[str: Union[str, int, float]]]:
        items: dict[str: Item] = self._store.items if not search else self.search_items(search)
        return {item_.product.prod_id: {'name': item_.product.name,
                                        'price': item_.product.price.amount,
                                        'price_format': item_.product.price.format(),
                                        'qty': item_.qty}
                for item_ in items.values()}

    @validate_arguments
    def get_sale_line_items(self) -> dict[str: dict[str: Union[str, int, float]]]:
        return {(sli.item.product.prod_id, sli.sale_price.amount): {'prod_id': sli.item.product.prod_id,
                                                                    'name': sli.item.product.name,
                                                                    'price': sli.sale_price.amount,
                                                                    'price_format': sli.sale_price.format(),
                                                                    'qty': sli.qty}
                for sli in self._sale.list_sli}

    @validate_arguments
    def search_items(self, text: str) -> dict[str: Item]:
        items = self._store.search_items_by_name(name=text)
        if text in self._store.items:  # search_items_by_id
            items[text] = self._store.items[text]
        return items

    @validate_arguments
    def put_on_sale(self, pr_id: str, qty: int, sale_price: float = None) -> None:
        sale_item = self._store.get_item_by_pr_id(pr_id)
        self._sale.add_line_item(item=sale_item, qty=qty, sale_price=sale_price)
        if sale_item.qty == 0:
            del self._store.items[sale_item.product.prod_id]

    @validate_arguments
    def is_item_exists(self, pr_id: str) -> bool:
        return pr_id in self._store.items

    @validate_arguments
    def get_item_qty_by_product_id(self, pr_id: str) -> int:
        if pr_id in self._store.items:
            return self._store.items[pr_id].qty

    @validate_arguments
    def put_item_form_sli_to_items(self, sli_id: str, sli_price: float) -> None:
        sli = self._sale.get_line_item_by_product_id_and_sale_price(sli_id, sli_price)
        self._sale.unset_line_item(sli=sli, qty=sli.qty)
        self._store.add_item(item=sli.item, qty=sli.qty)

    @validate_arguments
    def edit_sale_price_in_sli(self, sli_product_id: str, old_sale_price: float, sale_price: float) -> None:
        sli = self._sale.get_line_item_by_product_id_and_sale_price(sli_product_id, old_sale_price)
        self._sale.edit_sale_price(sli, sale_price)

    def get_store_places_of_sale_names(self) -> list[str]:
        return [place_of_sale.name for place_of_sale in self._store.places_of_sale]

    def get_store_sellers_names(self) -> list[str]:
        return [seller.name for seller in self._store.sellers]

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
            self._store.places_of_sale[current_place_of_sale_id].sale = self._sale
            self._sale.seller = self._store.sellers[current_seller_id]
            self._sale.completed()
            return True
        return False


if __name__ == '__main__':
    handler = SaleRegistrationHandler(test=True)

    for key, item in sorted(handler.get_store_items().items()):
        print(key, item)
