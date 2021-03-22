from prjstore.domain.store import Store
from prjstore.domain.test.test_item import TestItem
from prjstore.domain.test.test_place_of_sale import TestPlaceOfSale
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from prjstore.domain.test.test_seller import TestSeller

class SaleRegistrationHandler:
    def __init__(self):
        self.store = Store()

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


if __name__ == '__main__':
    handler = SaleRegistrationHandler()
    handler.test()
    for key, item in handler.store.items.items():
        print(item.product.name)
    # for place in handler.store.places_of_sale:
    #     if place.sale:
    #         print(place.sale.line_items)
