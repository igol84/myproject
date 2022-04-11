from typing import Optional

from pydantic import validate_arguments

from prjstore.db import API_DB
from prjstore.db.schemas import handler_items_editor as db_schemas
from prjstore.domain.item import Item
from prjstore.domain.store import Store
from prjstore.handlers.data_for_test.sale_registration import put_test_data_to_store
from prjstore.ui.pyside.items_editor import schemas


class ItemsEditorHandler:
    __db: API_DB
    __store: Store

    def __init__(self, db: API_DB = None, test=False, store=None):
        self.__db = db
        if test:
            self.__store = Store(id=1, name='test')
            put_test_data_to_store(self.__store)
        else:
            self.store_id = db.headers['store_id']
            self.update_data(store)

    def get_store(self):
        return self.__store

    store = property(get_store)

    def update_data(self, store: Store):
        if not store:
            self.__store = Store.create_from_schema(self.__db.store.get(id=self.store_id))
        else:
            self.__store = store

    def get_store_items(self, search: Optional[str] = None) -> list[schemas.ViewItem]:
        items: dict[int: Item] = self.__store.items if not search else self.search_items(search)
        list_pd_items = []
        for item in items.values():
            desc = item.product.name
            if item.product.product_type == 'shoes':
                desc += f' {item.product.color}' if item.product.color else ''
                desc += f' {item.product.width.short_name}' if item.product.width else ''
                desc += f' {item.product.size:g}'
            price = item.buy_price.amount
            date_buy = item.date_buy
            pd_item = schemas.ViewItem(item_id=item.id, desc=desc, price_buy=price, qty=item.qty, date_buy=date_buy)
            list_pd_items.append(pd_item)
            list_pd_items.sort(key=lambda k: k.item_id, reverse=True)

        return list_pd_items

    @validate_arguments
    def search_items(self, text: str) -> dict[str: Item]:
        return self.__store.search_items(value=text, fields={'name', 'prod_id'})

    def edit_item(self, data: db_schemas.ItemFormEdit):
        # edit on DB
        new_data: db_schemas.ItemFormEdit = self.__db.handler_items_editor.edit_item(data)
        # edit in Domain Model
        item = self.__store.items[data.id]
        item.qty = data.new_qty
        item.buy_price.amount = data.new_price
        return new_data

    def delete_item(self, item_id: int) -> None:
        # edit on DB
        self.__db.handler_items_editor.del_item(item_id)
        # edit in Domain Model
        del self.__store.items[item_id]

    def get_item_sales(self, item_id: int) -> list[db_schemas.SaleDetail]:
        return self.__db.handler_items_editor.get_item_sales(item_id)
