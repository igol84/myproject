from unittest import TestCase

from prjstore.domain.item import Item
from prjstore.domain.test.test_products_catalog import TestProductCatalog


class TestItem(TestCase):

    def setUp(self) -> None:
        self.pc = []
        TestProductCatalog.setUp(self)
        self.items = {'1': Item(pr=self.pc['1']),
                      '3': Item(pr=self.pc['3'], qty=2),
                      '6': Item(pr=self.pc['6'], buy_price=100.5),
                      '2': Item(pr=self.pc['2'], qty=3, buy_price=200)}

    def test_01_initial(self):
        self.assertEqual(str(self.items['2']), '<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>')
        self.assertEqual(str(self.items['2'].product), '<SimpleProduct: id=2, name=item23, price=UAH 600.00>')

    def test_02_edit(self):
        self.items['2'].product=self.pc['3']

        self.assertEqual(str(self.items['2']), '<Item: product=<Shoes: id=3, name=item24, price=UAH 700.00, color=red, '
                                             'size=43.3, length_of_insole=28.0, width=Medium>, qty=3>')

    def test_03_edit_qty(self):
        self.items['2'].qty = 1
        self.assertEqual(self.items['1'].qty, 1)

    def test_04_edit_price(self):
        self.assertEqual(str(self.items['1'].buy_price), 'UAH 0.00')
        self.items['1'].buy_price = 200
        self.assertEqual(str(self.items['1'].buy_price), 'UAH 200.00')

