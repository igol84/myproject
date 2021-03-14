from unittest import TestCase

from prjstore.domain.sale_line_item import SaleLineItem
from prjstore.domain.test.test_item import TestItem


class TestSaleLineItem(TestCase):
    def setUp(self) -> None:
        self.items=[]
        TestItem.setUp(self)
        self.list_sli = [SaleLineItem(self.items['2']),
                           SaleLineItem(self.items['1']),
                           SaleLineItem(self.items['3'])]

    def test_01_initial(self):
        self.assertEqual(str(self.list_sli[0]),
                         '<SaleLineItem: item='
                         '<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, '
                         'sale_price=UAH 600.00, qty=1>')
        self.assertEqual(str(self.list_sli[1]),
                         '<SaleLineItem: item=<Item: product='
                         '<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0, length_of_insole=11.0,'
                         ' width=Medium>, qty=1>, sale_price=UAH 100.00, qty=1>')

    def test_02_edit_qty(self):
        self.list_sli[0].qty = 3
        self.assertEqual(self.list_sli[0].qty, 3)

    def test_03_edit_sale_price(self):
        self.list_sli[0].sale_price = 500
        self.assertEqual(str(self.list_sli[0].sale_price), 'UAH 500.00')

    def test_04_assert_qty(self):
        self.assertRaises(AssertionError, SaleLineItem, item=self.items['1'], qty=2)
        with self.assertRaises(AssertionError):
            self.list_sli[1].qty = 3
