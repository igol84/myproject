from unittest import TestCase

from prjstore.domain.store import Store
from prjstore.domain.test.test_item import TestItem
from prjstore.domain.test.test_place_of_sale import TestPlaceOfSale
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from prjstore.domain.test.test_seller import TestSeller


class TestStore(TestCase):
    def setUp(self) -> None:
        self.store = Store()
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


class Test_Store(TestStore):
    def test_01_pc(self):
        self.assertEqual(len(self.store.pc), 5)
        self.assertEqual(self.store.pc['1'].name, 'item1')

    def test_02_items(self):
        self.assertEqual(len(self.store.items), 4)
        self.assertEqual(self.store.items['2'].product.name, 'item23')

    def test_03_sellers(self):
        self.assertEqual(len(self.store.sellers), 3)
        self.assertEqual(self.store.sellers[2].name, 'Sasha')

    def test_04_places_of_sale(self):
        self.assertEqual(len(self.store.places_of_sale), 4)
        self.assertEqual(str(self.store.places_of_sale[0].sale.line_items[0].item.product.name), 'item1')

    def test_04_get_item_by_pr_id(self):
        self.assertEqual(self.store.get_item_by_pr_id('2').product.name, 'item23')

    def test_05_search_item(self):
        self.assertEqual(len(self.store.search_item(name = 'item2')), 3)
