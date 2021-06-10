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
        self.sale.add_line_item(self.items['3'], sale_price=(200))
        self.sale.date_time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')

class Test_Sale(TestSale):
    def test_01_initial(self):
        sale = Sale(seller=Seller('Igor'))
        sale.date_time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')
        self.assertEqual(str(sale.seller.name), 'Igor')
        self.assertEqual(str(sale.list_sli), '[]')
        self.assertEqual(str(sale.date_time), '2020-06-06 12:19:55')

    def test_get_list_sli(self):
        list_sli = [(sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount) for sli in self.sale.list_sli]
        self.assertEqual(str(list_sli),
                         "[('item1', 0, 1, 100.0), ('item23', 1, 2, 600.0), ('item24', 1, 1, 200.0)]")

    def test_add_line_item(self):
        sli = [(sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount) for sli in self.sale['2']]
        self.assertEqual(str(sli),
                         "[('item23', 1, 2, 600.0)]")
        self.sale.add_line_item(self.items['2'], sale_price=700)
        sli = [(sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount) for sli in self.sale['2']]
        self.assertEqual(str(sli),
                         "[('item23', 0, 2, 600.0), ('item23', 0, 1, 700.0)]")
        with self.assertRaises(AssertionError):
            self.sale.add_line_item(self.items['2'], sale_price=700)

    def test_add_line_item_2(self):
        self.sale.add_line_item(self.items['2'], qty=1)
        sli = self.sale[('2', 600)]
        sli = [sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount]
        self.assertEqual(str(sli),
                         "['item23', 0, 3, 600.0]")


    def test_get_line_item_by_product_id(self):
        sli = self.sale.get_line_item_by_product_id_and_sale_price('2', 600)
        sli = [sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount]
        self.assertEqual(str(sli),
                         "['item23', 1, 2, 600.0]")

    def test_unset_line_item_by_pr_id(self):
        self.sale.unset_line_item_by_pr_id_and_sale_price('2', 600)
        self.assertEqual(self.sale[('2', 600)].qty, 1)
        self.sale.unset_line_item_by_pr_id_and_sale_price('2', 600)
        self.assertEqual(self.sale[('2', 600)], None)

    def test_del_line_item_by_product_id(self):
        self.sale.del_line_item_by_product_id_and_sale_price('2', 600)
        self.assertEqual(self.sale.get_line_item_by_product_id_and_sale_price('2', 600), None)


    def test_del_line_item_by_product_id_2(self):
        del self.sale[('2', 600)]
        self.assertEqual(self.sale.get_line_item_by_product_id_and_sale_price('2', 600), None)

    def test_is_complete(self):
        self.assertEqual(self.sale.is_complete(), False)

    def test_completed(self):
        self.sale.completed()
        self.assertEqual(self.sale.is_complete(), True)

    def test_get_time(self):
        self.assertEqual(str(self.sale.date_time), '2020-06-06 12:19:55')

    def test_set_time(self):
        self.sale.date_time = datetime.datetime.strptime('6/6/20, 12:20:55', '%m/%d/%y, %H:%M:%S')
        self.assertEqual(str(self.sale.date_time), '2020-06-06 12:20:55')

    def test_get_seller(self):
        self.assertEqual(str(self.sale.seller.name), 'Igor')

    def test_set_seller(self):
        self.sale.seller = Seller('Anna')
        self.assertEqual(str(self.sale.seller.name), 'Anna')

    def test_is_item_in_sale(self):
        self.assertEqual(self.sale.is_item_in_sale(self.items['6']), False)
        self.assertEqual(self.sale.is_item_in_sale(self.items['2']), True)

    def test_is_product_in_sale(self):
        self.assertEqual(self.sale.is_product_in_sale(self.items['6'].product), False)
        self.assertEqual(self.sale.is_product_in_sale(self.items['2'].product), True)
