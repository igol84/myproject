import datetime
from unittest import TestCase

from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.sale import Sale
from prjstore.domain.seller import Seller
from prjstore.domain.test.test_sale import TestSale


class TestPlaceOfSale(TestCase):
    def setUp(self) -> None:
        self.items = []
        self.sale = None
        TestSale.setUp(self)
        self.places_of_sale = [PlaceOfSale('Интернет'), PlaceOfSale('Бокс 47'), 
                               PlaceOfSale('Магазин 1-й этаж'), PlaceOfSale('Магазин 2-й этаж')]
        self.places_of_sale[0].sale = self.sale

class Test_PlaceOfSale(TestPlaceOfSale):
    def test_initial(self):
        place_of_sale = PlaceOfSale('Бокс 47')
        self.assertEqual(str(place_of_sale), '<PlaceOfSale: name: Бокс 47, sale:No>')
        self.assertEqual(place_of_sale.name,'Бокс 47')

    def test_edit_name(self):
        self.places_of_sale[0].name = 'Магазин 2-й этаж'
        self.assertEqual(self.places_of_sale[0].name, 'Магазин 2-й этаж')

    def test_make_new_sale(self):
        self.places_of_sale[0].make_new_sale(Sale(seller=Seller('Igor')))
        self.places_of_sale[0].sale.time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')
        self.assertEqual(str(self.places_of_sale[0].sale),
                         '<Sale: seller:Igor, time: 06/06/2020, 12:19:55, not completed, line items:\n >')

    def test_set_items_on_sale(self):
        self.places_of_sale[0].set_items_on_sale(self.items['2'])
        self.assertEqual(str(self.places_of_sale[0].sale['2']),
            '<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>'
            ', qty=3>, sale_price=UAH 600.00, qty=3>')

    def test_set_items_on_sale_by_pr_id(self):
        self.places_of_sale[0].set_items_on_sale_by_pr_id('2')
        self.assertEqual(str(self.places_of_sale[0].sale['2']),
                         '<SaleLineItem: item=<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>'
                         ', qty=3>, sale_price=UAH 600.00, qty=3>')

    def test_unset_items_on_sale_by_pr_id(self):
        self.places_of_sale[0].unset_items_on_sale_by_pr_id('2')
        self.assertEqual(self.places_of_sale[0].sale['2'].qty, 1)
        self.places_of_sale[0].unset_items_on_sale_by_pr_id('2')
        with self.assertRaises(IndexError):
            self.places_of_sale[0].sale.get_line_item_by_product_id('2')

    def test_end_sale_items(self):
        self.places_of_sale[0].end_sale_items()
        self.assertEqual(self.places_of_sale[0].sale, None)
