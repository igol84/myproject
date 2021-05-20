import datetime
from unittest import TestCase

from prjstore.domain.sale import Sale
from prjstore.domain.seller import Seller
from prjstore.domain.test.test_item import TestItem


class TestSale(TestCase):
    def setUp(self) -> None:
        self.items=[]
        TestItem.setUp(self)
        self.sale = Sale(Seller('Igor'))
        self.sale.add_line_item(self.items['1'])
        self.sale.add_line_item(self.items['2'], qty=2)
        self.sale.add_line_item(self.items['3'])
        self.sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')

class Test_Sale(TestSale):
    def test_01_initial(self):
        sale = Sale(seller=Seller('Igor'))
        sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')
        self.assertEqual(str(sale),
                         '<Sale: seller:Igor, time: 06/06/2020, 12:19:55, not completed, line items:\n >')

    def test_02_initial(self):
        self.items=[]
        TestItem.setUp(self)
        sale = Sale(Seller('Igor'), self.items['1'])
        sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')
        self.assertEqual(str(sale),
                '<Sale: seller:Igor, time: 06/06/2020, 12:19:55, not completed, line items:\n'
                ' <SaleLineItem: item=<Item: product=<Shoes: id=1, name=item1, price=UAH 100.00, color=default,'
                ' size=36.0, length_of_insole=11.0, width=Medium>, qty=1>, sale_price=UAH 100.00, qty=1>>')

    def test_03_initial(self):
        self.items=[]
        TestItem.setUp(self)
        sale = Sale(seller=Seller('Igor'), item=self.items['2'], gty=2)
        sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')
        self.assertEqual(str(sale),
                '<Sale: seller:Igor, time: 06/06/2020, 12:19:55, not completed, line items:\n'
                ' <SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,'
                ' sale_price=UAH 600.00, qty=2>>')

    def test_get_list_sli(self):
        list_sli = self.sale.get_list_sli()
        self.assertEqual(str(list_sli),
            '[<SaleLineItem: item=<Item: product=<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0,'
            ' length_of_insole=11.0, width=Medium>, qty=1>, sale_price=UAH 100.00, qty=1>, <SaleLineItem: item='
            '<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, sale_price=UAH 600.00, qty=2>'
            ', <SaleLineItem: item=<Item: product=<Shoes: id=3, name=item24, price=UAH 700.00, color=red, size=43.3,'
            ' length_of_insole=28.0, width=Medium>, qty=2>, sale_price=UAH 700.00, qty=1>]')

    def test_add_line_item(self):
        self.sale.add_line_item(self.items['2'])
        self.assertEqual(str(self.sale['2']),
                         '<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, '
                         'qty=3>, sale_price=UAH 600.00, qty=3>')

    def test_add_line_item_2(self):
        self.sale.add_line_item(self.items['2'], qty=1)
        self.assertEqual(str(self.sale['2']),
                         '<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, '
                         'qty=3>, sale_price=UAH 600.00, qty=3>')

    def test_add_line_item_by_product_id(self):
        self.sale.add_line_item_by_product_id('2')
        self.assertEqual(str(self.sale['2']),
                         '<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, '
                         'qty=3>, sale_price=UAH 600.00, qty=3>')

    def test_add_line_item_by_product_id_2(self):
        self.sale.add_line_item_by_product_id(pr_id='2', qty=1)
        self.assertEqual(str(self.sale['2']),
                         '<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, '
                         'qty=3>, sale_price=UAH 600.00, qty=3>')

    def test_get_line_item_by_product_id(self):
        sli = self.sale.get_line_item_by_product_id('2')
        self.assertEqual(str(sli),
                         '<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, '
                         'qty=3>, sale_price=UAH 600.00, qty=2>')

    def test_unset_line_item_by_pr_id(self):
        self.sale.unset_line_item_by_pr_id('2')
        self.assertEqual(self.sale['2'].qty, 1)
        self.sale.unset_line_item_by_pr_id('2')
        with self.assertRaises(IndexError):
            self.sale.get_line_item_by_product_id('2')

    def test_del_line_item_by_product_id(self):
        self.sale.del_line_item_by_product_id('2')
        with self.assertRaises(IndexError):
            self.sale.get_line_item_by_product_id('2')

    def test_del_line_item_by_product_id_2(self):
        del self.sale['2']
        with self.assertRaises(IndexError):
            self.sale.get_line_item_by_product_id('2')

    def test_is_complete(self):
        self.assertEqual(self.sale.is_complete(), False)

    def test_completed(self):
        self.sale.completed()
        self.assertEqual(self.sale.is_complete(), True)

    def test_get_time(self):
        self.assertEqual(str(self.sale.get_date_time()), '2020-06-06 12:19:55')

    def test_set_time(self):
        self.sale.set_date_time(datetime.datetime.strptime('6/6/20, 12:20:55', '%m/%d/%y, %H:%M:%S'))
        self.assertEqual(str(self.sale.get_date_time()), '2020-06-06 12:20:55')

    def test_get_seller(self):
        self.assertEqual(str(self.sale.get_seller()), '<Seller: name=Igor>')

    def test_set_seller(self):
        self.sale.set_seller(Seller('Anna'))
        self.assertEqual(str(self.sale.get_seller()), '<Seller: name=Anna>')

    def test_is_item_in_sale(self):
        self.assertEqual(self.sale.is_item_in_sale(self.items['6']), False)
        self.assertEqual(self.sale.is_item_in_sale(self.items['2']), True)

    def test_is_product_in_sale(self):
        self.assertEqual(self.sale.is_product_in_sale(self.items['6'].product), False)
        self.assertEqual(self.sale.is_product_in_sale(self.items['2'].product), True)
