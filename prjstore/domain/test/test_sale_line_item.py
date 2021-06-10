from unittest import TestCase

from prjstore.domain.sale_line_item import SaleLineItem
from prjstore.domain.test.test_item import TestItem
from util.money import Money


class TestSaleLineItem(TestCase):
    def setUp(self) -> None:
        self.items = []
        TestItem.setUp(self)
        self.list_sli = [SaleLineItem(self.items['2']),
                         SaleLineItem(item=self.items['1'], sale_price=(250,)),
                         SaleLineItem(self.items['3'], sale_price=(750,), qty=2)]


class Test_SaleLineItem(TestSaleLineItem):
    def test_01_initial(self):
        self.assertEqual(str(self.list_sli[0].item.product.name), 'item23')
        self.assertEqual(str(self.list_sli[0].qty), '1')
        self.assertEqual(str(self.list_sli[0].sale_price.amount), '600.0')
        self.assertEqual(str(self.list_sli[2].item.product.name), 'item24')
        self.assertEqual(str(self.list_sli[2].qty), '2')
        self.assertEqual(str(self.list_sli[2].sale_price.amount), '750.0')


    def test_02_edit_qty(self):
        self.list_sli[0].qty = 3
        self.assertEqual(self.list_sli[0].qty, 3)

    def test_03_edit_sale_price(self):
        self.list_sli[0].sale_price = Money(500)
        self.assertEqual(str(self.list_sli[0].sale_price.amount), '500.0')

