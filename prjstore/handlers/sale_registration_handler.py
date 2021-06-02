import datetime

from PySide2.QtWidgets import QMessageBox

from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.sale import Sale
from prjstore.domain.sale_line_item import SaleLineItem
from prjstore.domain.store import Store
from prjstore.domain.test.test_item import TestItem
from prjstore.domain.test.test_place_of_sale import TestPlaceOfSale
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from prjstore.domain.test.test_seller import TestSeller


class SaleRegistrationHandler:
    def __init__(self):
        self.store = Store()
        self.sale = Sale()
        self.current_place_of_sale = None

    def test(self):
        self.pc = None
        TestProductCatalog.setUp(self)
        self.store.pc = self.pc
        self.items = {}
        TestItem.setUp(self)
        self.store.items = self.items
        self.sellers = []
        TestSeller.setUp(self)
        self.store.sellers = self.sellers
        self.places_of_sale = []
        TestPlaceOfSale.setUp(self, sale=False)
        self.store.places_of_sale = self.places_of_sale
        self.store.places_of_sale[0].sale = None
        self.store.items['1'].qty = 150
        self.store.items['1'].product.price = 10500
        self.store.items['1'].product.name = 'Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!'

    def get_store_items(self, search=None) -> dict[str: dict]:
        items: dict[str: Item] = self.store.items if not search else self.search_items(search)
        return {item.product.id:
                    {'name': item.product.name,
                     'price': item.product.price.amount,
                     'price_format': item.product.price.format_my(),
                     'qty': item.qty}
                for item in items.values()}

    def get_sale_line_items(self) -> dict[str: dict]:
        return {(sli.item.product.id, sli.sale_price.amount):
                    {'id': sli.item.product.id,
                     'name': sli.item.product.name,
                     'price': sli.sale_price.amount,
                     'price_format': sli.sale_price.format_my(),
                     'qty': sli.qty}
                for sli in self.sale.line_items}

    def search_items(self, text: str) -> dict[str: Item]:
        items = self.store.search_items_by_name(name=text)
        if text in self.store.items:  # search_items_by_id
            items[text] = self.store.items[text]
        return items

    def put_on_sale(self, pr_id: str, qty: int, sale_price: float = None):
        sale_item = self.store.get_item_by_pr_id(pr_id)
        self.sale.add_line_item(item=sale_item, qty=qty, sale_price=sale_price)
        if sale_item.qty == 0:
            del self.store.items[sale_item.product.id]

    def is_item_exists(self, pr_id):
        return pr_id in self.store.items

    def get_item_qty_by_product_id(self, pr_id: str) -> int:
        if pr_id in self.store.items:
            return self.store.items[pr_id].qty

    def put_item_form_sli_to_items(self, sli_id: str, sli_price: float):
        sli = self.sale.get_line_item_by_product_id_and_sale_price(sli_id, sli_price)
        self.sale.unset_line_item(sli=sli, qty=sli.qty)
        self.store.add_item(item=sli.item, qty=sli.qty)

    def edit_sale_price_in_sli(self, sli_product_id: str, old_sale_price: float, sale_price: float):
        sli = self.sale.get_line_item_by_product_id_and_sale_price(sli_product_id, old_sale_price)
        self.sale.edit_sale_price(sli, sale_price)

    def change_date(self, date: datetime.date):
        time = datetime.datetime.min.time()
        date_time = datetime.datetime.combine(date, time)
        self.sale.date_time = date_time

    def get_store_places_of_sale_names(self):
        return [place_of_sale.name for place_of_sale in self.store.places_of_sale]

    def change_place_of_sale(self, place_of_sale_id: int):
        self.store.places_of_sale[place_of_sale_id].sale = self.sale
        if self.current_place_of_sale:
            self.current_place_of_sale.sale = None
        self.current_place_of_sale = self.store.places_of_sale[place_of_sale_id]

    def get_store_sellers_names(self):
        return [seller.name for seller in self.store.sellers]

    def change_seller(self, seller_id: int):
        current_seller = self.sellers[seller_id]
        self.sale.seller = current_seller

    def press_save_button(self):
        if self.current_place_of_sale and self.sale.seller and self.sale.line_items:
            self.sale.completed()
            if self.sale.is_complete():
                QMessageBox(icon=QMessageBox.Information, text='Продажа выполнена!').exec_()
        else:
            warning_texts = []
            if not self.current_place_of_sale:
                warning_texts.append('Не вабрано место продажи!')
            if not self.sale.seller:
                warning_texts.append('Не вабран продавец!')
            if not self.sale.line_items:
                warning_texts.append('Нет товаров в списке продаж!')
            QMessageBox(icon=QMessageBox.Warning, text='\n'.join(warning_texts)).exec_()


if __name__ == '__main__':
    handler = SaleRegistrationHandler()
    handler.test()

    for key, item in handler.store.items.items():
        print(item.product.name)
    # for place in handler.store.places_of_sale:
    #     if place.sale:
    #         print(place.sale.line_items)
