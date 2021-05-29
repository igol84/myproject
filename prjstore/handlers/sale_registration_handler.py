import datetime

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

    def search_items(self, text: str) -> dict[str: Item]:
        items = self.store.search_items_by_name(name=text)
        if text in self.store.items:  # search_items_by_id
            items[text] = self.store.items[text]
        return items

    def put_on_sale(self, item: Item, qty: int, sale_price: float = None):
        self.sale.add_line_item(item=item, qty=qty, sale_price=sale_price)
        if item.qty == 0:
            del self.store.items[item.product.id]

    def put_item_form_sli_to_items(self, sli: SaleLineItem):
        self.sale.unset_line_item(sli=sli, qty=sli.qty)
        self.store.add_item(item=sli.item, qty=sli.qty)

    def edit_sale_price_in_sli(self, sli, sale_price: float):
        self.sale.edit_sale_price(sli, sale_price)

    def change_date(self, date: datetime.date):
        time = datetime.datetime.min.time()
        date_time = datetime.datetime.combine(date, time)
        self.sale.date_time = date_time

    def change_place_of_sale(self, place_of_sale_id: int):
        self.store.places_of_sale[place_of_sale_id].sale = self.sale
        if self.current_place_of_sale:
            self.current_place_of_sale.sale = None
        self.current_place_of_sale = self.store.places_of_sale[place_of_sale_id]

    def change_seller(self, seller_id: int):
        current_seller = self.sellers[seller_id]
        self.sale.seller = current_seller

    def press_save_button(self):
        if self.current_place_of_sale and self.sellers and self.sale.line_items:
            self.sale.completed()
            print(self.store)
            print(self.sale)
        else:
            print('Не все условия выполнены')

if __name__ == '__main__':
    handler = SaleRegistrationHandler()
    handler.test()

    for key, item in handler.store.items.items():
        print(item.product.name)
    # for place in handler.store.places_of_sale:
    #     if place.sale:
    #         print(place.sale.line_items)
