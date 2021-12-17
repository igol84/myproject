import datetime
from typing import Optional

from pydantic import validate_arguments

from prjstore.db import API_DB
from prjstore.domain.item import Item
from prjstore.domain.sale import Sale
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data
from prjstore.ui.pyside.sale_registration.schemas import (
    ModelProduct, create_product_schemas_by_items, create_sli_schemas_by_items, ProductId, Price,
    create_sales_by_sales_schemas, create_sale_schemas_by_ledger, ViewSale, ModelSale
)


class SaleRegistrationHandler:
    __db: API_DB
    __store: Store
    __sale: Sale
    __ledger: dict[int, ModelSale]

    def __init__(self, db: API_DB = None, store_id=1, test=False):
        self.__db = db
        self.__sale = Sale()
        self.test_mode = test
        if test:
            self.__store = Store(id=store_id, name='test')
            put_test_data(self)
        else:
            self.__store = Store.create_from_schema(self.__db.store.get(id=1))
            self.update_store_sales_by_date(date=datetime.datetime.now().date())

    def get_sale(self):
        return self.__sale

    sale = property(get_sale)

    def get_store(self):
        return self.__store

    store = property(get_store)

    def get_ledger(self):
        return self.__ledger

    ledger = property(get_ledger)

    @validate_arguments
    def get_store_items(self, search: Optional[str] = None) -> list[ModelProduct]:
        products: dict[int: Item] = self.store.items if not search else self.search_items(search)
        return create_product_schemas_by_items(products)

    @validate_arguments
    def update_store_sales_by_date(self, date: datetime.date, place_id: int = None, seller_id: int = None) -> None:
        pd_sales = self.__db.sale.get_all(store_id=self.store.id, date=date, place_id=place_id, seller_id=seller_id)
        self.__ledger = create_sales_by_sales_schemas(pd_sales)

    @validate_arguments
    def changed_date(self, date: datetime.date, place_id: int = None, seller_id: int = None) -> None:
        self.update_store_sales_by_date(date=date, place_id=place_id, seller_id=seller_id)

    @validate_arguments
    def get_sale_line_items(self, sale_id: int = None) -> dict[tuple[ProductId, Price]: ModelProduct]:
        list_sli = self.ledger[sale_id].sale.list_sli if sale_id else self.sale.list_sli
        return create_sli_schemas_by_items(list_sli)

    def get_old_sales(self) -> list[ViewSale]:
        return create_sale_schemas_by_ledger(self.ledger)

    @validate_arguments
    def search_items(self, text: str) -> dict[str: Item]:
        return self.store.search_items(value=text, fields={'name', 'prod_id'})

    @validate_arguments
    def put_on_sale(self, pr_id: str, qty: int, sale_price: float = None) -> None:
        sale_items = self.store.get_items_by_pr_id(pr_id)
        qty_need_to_add = qty
        for sale_item in sale_items:
            qty_line_item = sale_item.qty if qty_need_to_add > sale_item.qty else qty_need_to_add
            self.__sale.add_line_item(item=sale_item, qty=qty_line_item, sale_price=sale_price)
            if sale_item.qty == 0:
                del self.store.items[sale_item.id]
            qty_need_to_add -= qty_line_item
            if qty_need_to_add == 0:
                break

    @validate_arguments
    def is_item_exists(self, pr_id: str) -> bool:
        return pr_id in self.store.items

    @validate_arguments
    def get_item_qty_by_product_id(self, pr_id: str) -> int:
        if pr_id in self.store.items:
            return self.store.items[pr_id].qty

    @validate_arguments
    def put_item_form_sli_to_items(self, pr_id: str, sli_price: float) -> None:
        sli_s = self.sale.get_line_items_by_product_id_and_sale_price(pr_id, sli_price)
        for sli in sli_s:
            self.sale.unset_line_item(sli=sli, qty=sli.qty)
            self.store.add_item(item=sli.item, qty=sli.qty)

    @validate_arguments
    def put_item_form_sli_to_items_in_old_sale(self, pr_id: str, sli_price: float, sale_id: int = None) -> None:
        tmp_sale = self.sale
        self.__sale = self.ledger[sale_id].sale
        sli_s = self.sale.get_line_items_by_product_id_and_sale_price(pr_id, sli_price)
        for sli in sli_s:
            self.__db.sale_line_item.delete(sale_id=sale_id, item_id=sli.item.id, sale_price=sli_price)
            self.sale.unset_line_item(sli=sli, qty=sli.qty)
            self.store.add_item(item=sli.item, qty=sli.qty)
        if not self.sale.list_sli:
            self.__db.sale.delete(sale_id)
            del self.__ledger[sale_id]
        self.__sale = tmp_sale

    @validate_arguments
    def edit_sale_price_in_sli(self, sli_product_id: str, old_sale_price: float, sale_price: float) -> None:
        sli_s = self.sale.get_line_items_by_product_id_and_sale_price(sli_product_id, old_sale_price)
        for sli in sli_s:
            self.sale.edit_sale_price(sli, sale_price)

    def get_store_places_of_sale_names(self) -> dict[int, str]:
        return {sale_id: place_of_sale.name for sale_id, place_of_sale in list(self.store.places_of_sale.items())}

    def get_store_sellers_names(self) -> dict[int, str]:
        return {seller_id: seller.name for seller_id, seller in list(self.store.sellers.items())}

    def get_total(self) -> str:
        total_str = ''
        if self.sale.list_sli:
            total = self.sale.get_total()
            total_purchase = self.sale.get_total_profit()
            total_str = f'Выручка: {total.format()}; Прибыль: {total_purchase.format()}'
        return total_str

    @validate_arguments
    def end_sale(self, date: datetime.date, current_place_of_sale_id: Optional[int],
                 current_seller_id: Optional[int]) -> bool:
        if current_place_of_sale_id is not None and current_seller_id is not None and self.__sale.list_sli:
            sale_time = datetime.datetime.now().time()
            self.sale.date_time = datetime.datetime.combine(date, sale_time)
            self.sale.seller = self.store.sellers[current_seller_id]
            current_place = self.store.places_of_sale[current_place_of_sale_id]
            current_place.sale = self.sale
            self.sale.completed()
            pd_sale = self.sale.schema_create(place_id=current_place_of_sale_id)
            if self.test_mode:
                return True
            if self.__db.sale.create(pd_sale):
                return True
        return False

    def is_complete(self):
        return self.__sale.is_complete()

    def new_sale(self):
        self.__sale = Sale()


if __name__ == '__main__':
    from pprint import pprint

    handler = SaleRegistrationHandler(test=True)
    for item in handler.get_store_items():
        pprint(item)
