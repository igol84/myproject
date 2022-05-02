import datetime
from typing import Optional

from pydantic import validate_arguments

from prjstore.db import API_DB, schemas
from prjstore.db.schemas import handler_sale_registration as handler_schemas
from prjstore.db.schemas.sale import ShowSaleWithSLIs
from prjstore.domain.item import Item
from prjstore.domain.sale import Sale
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.sale_registration.schemas import (
    ModelProduct, create_product_schemas_by_items, create_sli_schemas_by_items, ProductId, Price,
    create_sale_schemas_by_places, ViewSale, ViewProduct
)
from util.money import Money


class SaleRegistrationHandler:
    __main_handler: Optional[MainHandler]
    __db: API_DB
    __store: Store
    __sale: Sale

    def __init__(self, db: API_DB = None, test=False, main_handler=None):
        self.__db = db
        self.__sale = Sale()
        self.__main_handler = main_handler
        self.test_mode = test
        self.store_id = None
        self.store_id = self.db.headers['store_id']
        if test:
            self.__store = Store(id=self.store_id, name='test')
            put_test_data(self)
        if not main_handler:
            self.__store = Store.create_from_schema(self.db.store.get(id=self.store_id))

    def __get_main_handler(self) -> Optional[MainHandler]:
        return self.__main_handler

    def __set_main_handler(self, main_handler: MainHandler) -> None:
        self.__main_handler = main_handler

    main_handler = property(__get_main_handler, __set_main_handler)

    def __get_store(self):
        if self.main_handler:
            store = self.main_handler.store
        else:
            store = self.__store
        return store

    store = property(__get_store)

    def __get_db(self):
        if self.main_handler:
            db = self.main_handler.db
        else:
            db = self.__db
        return db

    db = property(__get_db)

    def __get_sale(self):
        return self.__sale

    sale = property(__get_sale)

    @validate_arguments
    def get_store_items(self, search: Optional[str] = None) -> list[ViewProduct]:
        products: dict[int: Item] = self.store.items if not search else self.search_items(search)
        return create_product_schemas_by_items(products)

    @validate_arguments
    def update_store_ledgers_by_date(self, date: datetime.date, place_id: int = None, seller_id: int = None) -> None:
        pd_sales: list[ShowSaleWithSLIs]
        for place in self.store.places_of_sale.values():
            for sale in place.ledger.values():
                if sale.date_time.date() == date:
                    return None
        pd_sales = self.db.sale.get_all(store_id=self.store.id, date=date, place_id=place_id, seller_id=seller_id)
        for pd_sale in pd_sales:
            sale = Sale.create_from_schema(pd_sale)
            self.store.places_of_sale[pd_sale.place.id].ledger[sale.id] = sale

    @validate_arguments
    def on_changed_date(self, date: datetime.date, place_id: int = None, seller_id: int = None) -> None:
        self.update_store_ledgers_by_date(date=date, place_id=place_id, seller_id=seller_id)

    @validate_arguments
    def get_sale_line_items(self, sale_id: int = None) -> dict[tuple[ProductId, Price]: ModelProduct]:
        list_sli = self.sale.list_sli
        if sale_id:
            for place in self.store.places_of_sale.values():
                if sale_id in place:
                    list_sli = place.ledger[sale_id].list_sli
                    break
        return create_sli_schemas_by_items(list_sli)

    def get_old_sales(self, date: datetime.date = None) -> list[ViewSale]:
        return create_sale_schemas_by_places(self.store.places_of_sale, date)

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
        for place in self.store.places_of_sale.values():
            if sale_id in place.ledger:
                self.__sale = place.ledger[sale_id]
                break
        sli_s = self.sale.get_line_items_by(pr_id, sli_price)
        list_del_items = []
        list_new_items = []
        list_update_items = []
        delete = False
        for sli in sli_s:
            pd_key = handler_schemas.SaleLineItemKeys(sale_id=sale_id, item_id=sli.item.id, sale_price=sli_price)
            list_del_items.append(pd_key)
            if sli.item.id not in self.store.items:
                pd_item = schemas.item.CreateItem(prod_id=pr_id, store_id=self.store.id, qty=sli.qty,
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
            for place in self.store.places_of_sale.values():
                if sale_id in place.ledger:
                    del place.ledger[sale_id]
                    break

        data = handler_schemas.PutItemFromOldSale(
            sale_id=sale_id, list_del_sli=list_del_items, list_new_items=list_new_items,
            list_update_items=list_update_items, delete=delete)
        self.db.header_sale_registration.put_items_from_old_sale(data=data)
        self.__sale = tmp_sale

    @validate_arguments
    def edit_sale_price_in_sli(self, sli_product_id: str, old_sale_price: float, new_sale_price: float) -> None:
        sli_s = self.sale.get_line_items_by(sli_product_id, old_sale_price)
        for sli in sli_s:
            self.sale.edit_sale_price(sli, new_sale_price)

    @validate_arguments
    def edit_sale_price_in_old_sli(self, sale_id: int, sli_prod_id: str, old_price: float, new_price: float):
        tmp_sale = self.sale
        for place in self.store.places_of_sale.values():
            if sale_id in place.ledger:
                self.__sale = place.ledger[sale_id]
                break
        sli_s = self.sale.get_line_items_by(sli_prod_id, old_price)
        for sli in sli_s:
            sli_schema = schemas.sale_line_item.SaleLineItem
            pd_sli_old = sli_schema(sale_id=self.sale.id, item_id=sli.item.id, sale_price=old_price, qty=sli.qty)
            pd_sli_new = sli_schema(sale_id=self.sale.id, item_id=sli.item.id, sale_price=new_price, qty=sli.qty)
            pd_data = schemas.handler_sale_registration.EditSLIPrice(old_sli=pd_sli_old, new_sli=pd_sli_new)
            self.db.header_sale_registration.edit_sli_price(data=pd_data)
            self.sale.edit_sale_price(sli, new_price)
        self.__sale = tmp_sale

    def get_store_places_of_sale_names(self) -> dict[int, str]:
        return {sale_id: place_of_sale.name for sale_id, place_of_sale in list(self.store.places_of_sale.items())
                if place_of_sale.active}

    def get_store_sellers_names(self) -> dict[int, str]:
        return {seller_id: seller.name for seller_id, seller in list(self.store.sellers.items()) if seller.active}

    def get_total(self, date: datetime.date) -> str:
        total: Money = None
        total_purchase: Money = None
        total_str = ''
        all_sales = [self.sale]
        for place in self.store.places_of_sale.values():
            for sale in place.ledger.values():
                if sale.date_time.date() == date:
                    all_sales.append(sale)
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
            db_end_sale = handler_schemas.EndSale(sale=pd_sale)
            if self.test_mode:
                return True
            new_sale: handler_schemas.OutputEndSale = self.db.header_sale_registration.end_sale(db_end_sale)
            if new_sale.sale:
                current_place = self.store.places_of_sale[current_place_of_sale_id]
                sale = Sale.create_from_schema(new_sale.sale)
                current_place.ledger[sale.id] = sale
                return True
        return False

    def is_complete(self):
        return self.__sale.is_complete()

    def new_sale(self):
        self.__sale = Sale()
