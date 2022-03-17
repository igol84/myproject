import datetime
from typing import Optional

from pydantic import validate_arguments

from prjstore.db import API_DB, schemas
from prjstore.db.schemas.handler_sale_registration import SaleLineItemKeys, PutItemFromOldSale
from prjstore.domain.item import Item
from prjstore.domain.sale import Sale
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data
from prjstore.ui.pyside.sale_registration.schemas import (
    ModelProduct, create_product_schemas_by_items, create_sli_schemas_by_items, ProductId, Price,
    create_sales_by_sales_schemas, create_sale_schemas_by_ledger, ViewSale, ModelSale, ViewProduct
)
from util.money import Money


class SaleRegistrationHandler:
    __db: API_DB
    __store: Store
    __sale: Sale
    __ledger: dict[int, ModelSale]

    def __init__(self, db: API_DB = None, test=False, store: Store = None):
        self.__db = db
        self.__sale = Sale()
        self.__ledger = {}
        self.test_mode = test
        self.store_id = None
        if db:
            self.store_id = db.headers['store_id']
        if test:
            self.__store = Store(id=self.store_id, name='test')
            put_test_data(self)
        else:
            self.update_data(store)

    def get_sale(self):
        return self.__sale

    sale = property(get_sale)

    def get_store(self):
        return self.__store

    store = property(get_store)

    def get_ledger(self):
        return self.__ledger

    ledger = property(get_ledger)

    def update_data(self, store: Store):
        self.__sale = Sale()
        self.__ledger = {}
        if store:
            self.__store = store
        else:
            self.__store = Store.create_from_schema(self.__db.store.get(id=self.store_id))

    @validate_arguments
    def get_store_items(self, search: Optional[str] = None) -> list[ViewProduct]:
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
        sli_s = self.sale.get_line_items_by(pr_id, sli_price)
        for sli in sli_s:
            self.sale.unset_line_item(sli=sli, qty=sli.qty)
            self.store.add_item(item=sli.item, qty=sli.qty)

    @validate_arguments
    def put_item_form_sli_to_items_in_old_sale(self, pr_id: str, sli_price: float, sale_id: int = None) -> None:
        tmp_sale = self.sale
        self.__sale = self.ledger[sale_id].sale
        sli_s = self.sale.get_line_items_by(pr_id, sli_price)
        list_del_items = []
        list_new_items = []
        list_update_items = []
        delete = False
        for sli in sli_s:
            list_del_items.append(SaleLineItemKeys(sale_id=sale_id, item_id=sli.item.id, sale_price=sli_price))
            if sli.item.id not in self.store.items:
                pd_item = schemas.item.CreateItem(prod_id=pr_id, store_id=sale_id, qty=sli.qty,
                                                  buy_price=sli.item.buy_price.amount, date_buy=sli.item.date_buy)
                list_new_items.append(pd_item)
            else:
                qty = self.store.items[sli.item.id].qty + sli.qty
                pd_item = schemas.item.UpdateItem(id=sli.item.id, prod_id=pr_id, store_id=self.store.id, qty=qty,
                                                  buy_price=sli.item.buy_price.amount, date_buy=sli.item.date_buy)
                list_update_items.append(pd_item)
            self.sale.unset_line_item(sli=sli, qty=sli.qty)
            self.store.add_item(item=sli.item, qty=sli.qty)
        if not self.sale.list_sli:
            delete = True
            del self.__ledger[sale_id]
        data = PutItemFromOldSale(sale_id=sale_id, list_del_sli=list_del_items, list_new_items=list_new_items,
                                  list_update_items=list_update_items, delete=delete)
        self.__db.header_sale_registration.put_items_from_old_sale(data=data)
        self.__sale = tmp_sale

    @validate_arguments
    def edit_sale_price_in_sli(self, sli_product_id: str, old_sale_price: float, new_sale_price: float) -> None:
        sli_s = self.sale.get_line_items_by(sli_product_id, old_sale_price)
        for sli in sli_s:
            self.sale.edit_sale_price(sli, new_sale_price)

    @validate_arguments
    def edit_sale_price_in_old_sli(self, sale_id: int, sli_prod_id: str, old_price: float, new_price: float):
        tmp_sale = self.sale
        self.__sale = self.ledger[sale_id].sale
        sli_s = self.sale.get_line_items_by(sli_prod_id, old_price)
        for sli in sli_s:
            sli_schema = schemas.sale_line_item.SaleLineItem
            pd_sli_old = sli_schema(sale_id=self.sale.id, item_id=sli.item.id, sale_price=old_price, qty=sli.qty)
            pd_sli_new = sli_schema(sale_id=self.sale.id, item_id=sli.item.id, sale_price=new_price, qty=sli.qty)
            pd_data = schemas.handler_sale_registration.EditSLIPrice(old_sli=pd_sli_old, new_sli=pd_sli_new)
            self.__db.header_sale_registration.edit_sli_price(data=pd_data)
            self.sale.edit_sale_price(sli, new_price)
        self.__sale = tmp_sale

    def get_store_places_of_sale_names(self) -> dict[int, str]:
        return {sale_id: place_of_sale.name for sale_id, place_of_sale in list(self.store.places_of_sale.items())}

    def get_store_sellers_names(self) -> dict[int, str]:
        return {seller_id: seller.name for seller_id, seller in list(self.store.sellers.items())}

    def get_total(self) -> str:
        total: Money = None
        total_purchase: Money = None
        total_str = ''
        all_sales = [self.sale]
        for model in self.ledger.values():
            all_sales.append(model.sale)
        for sale in all_sales:
            if sale.list_sli:
                total = total + sale.get_total() if total else sale.get_total()
                total_purchase = total_purchase + sale.get_total_profit() if total_purchase else sale.get_total_profit()
        if total:
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
            if new_sale := self.__db.sale.create(pd_sale):
                self.__ledger.update(create_sales_by_sales_schemas([new_sale]))
                return True
        return False

    def is_complete(self):
        return self.__sale.is_complete()

    def new_sale(self):
        self.__sale = Sale()
