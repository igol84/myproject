from prjstore.domain.test.test_item import TestItem
from prjstore.domain.test.test_place_of_sale import TestPlaceOfSale
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from prjstore.domain.test.test_seller import TestSeller
from util.money import Money


def put_test_data(handler):
    test = TestProductCatalog()
    test.setUp()
    handler._store.pc = test.pc
    test = TestItem()
    test.setUp()
    handler._store.items = test.items
    test = TestSeller()
    test.setUp()
    handler._store.sellers = test.sellers
    test = TestPlaceOfSale()
    test.setUp(sale=False)
    handler._store.places_of_sale = test.places_of_sale
    handler._store.places_of_sale[1].sale = None
    handler._store.items[1].qty = 150
    handler._store.items[1].product.price = Money(10500)
    handler._store.items[1].product.name = 'Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!'
