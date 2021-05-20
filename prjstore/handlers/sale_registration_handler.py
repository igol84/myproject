from prjstore.domain.item import Item
from prjstore.domain.sale import Sale
from prjstore.domain.store import Store
from prjstore.domain.test.test_item import TestItem
from prjstore.domain.test.test_place_of_sale import TestPlaceOfSale
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from prjstore.domain.test.test_seller import TestSeller


class SaleRegistrationHandler:
    def __init__(self):
        self.store = Store()
        self.sale = Sale()

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
        TestPlaceOfSale.setUp(self)
        self.store.places_of_sale = self.places_of_sale
        self.store.items['1'].qty = 150
        self.store.items['1'].product.price = 10500
        self.store.items['1'].product.name = 'Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!'

    def search_items(self, text: str) ->  dict[str: Item]:
        items = self.store.search_items_by_name(name=text)
        if text in self.store.items: # search_items_by_id
            items[text] = self.store.items[text]
        return items

    def put_on_sale(self, item: Item, qty: int):
        self.sale.add_line_item(item=item, qty=qty)
        print(item, qty)
        if item.qty > qty:
            item.qty -= qty
        else:
            del item



if __name__ == '__main__':
    handler = SaleRegistrationHandler()
    handler.test()

    for key, item in handler.store.items.items():
        print(item.product.name)
    # for place in handler.store.places_of_sale:
    #     if place.sale:
    #         print(place.sale.line_items)
