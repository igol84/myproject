from unittest import TestCase

from prjstore.domain.item import Item
from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from util.money import Money


class TestItem(TestCase):

    def setUp(self) -> None:
        self.pc = ProductCatalog()
        TestProductCatalog.setUp(self)
        self.items = {'1': Item(product=self.pc.products['1']),
                      '3': Item(product=self.pc.products['3'], qty=2),
                      '6': Item(product=self.pc.products['6'], buy_price=(100.5,)),
                      '2': Item(product=self.pc.products['2'], qty=3, buy_price=(200,))}

class Test_Item(TestItem):
    def test_01_initial(self):
        self.assertEqual(str(self.items['2'].product.name), 'item23')
        self.assertEqual(str(self.items['2'].qty), '3')
        self.assertEqual(str(self.items['2'].buy_price.amount), '200.0')

    def test_02_edit(self):
        self.items['2'].product=self.pc['3']
        self.assertEqual(str(self.items['2'].product.name), 'item24')
        self.assertEqual(str(self.items['2'].qty), '3')
        self.assertEqual(str(self.items['2'].buy_price.amount), '200.0')

    def test_03_edit_qty(self):
        self.items['2'].qty = 1
        self.assertEqual(self.items['1'].qty, 1)

    def test_04_edit_price(self):
        self.assertEqual(str(self.items['1'].buy_price.amount), '0.0')
        self.items['1'].buy_price = Money(200)
        self.assertEqual(str(self.items['1'].buy_price.amount), '200.0')

