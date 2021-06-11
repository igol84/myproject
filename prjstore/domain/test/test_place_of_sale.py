import datetime
from unittest import TestCase

from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.sale import Sale
from prjstore.domain.seller import Seller
from prjstore.domain.test.test_sale import TestSale


class TestPlaceOfSale(TestCase):
    def setUp(self, sale = True) -> None:
        self.items = []
        if sale == True:
            TestSale.setUp(self)
        else:
            self.sale = Sale()
        self.places_of_sale = [PlaceOfSale('Интернет'), PlaceOfSale('Бокс 47'), 
                               PlaceOfSale('Магазин 1-й этаж'), PlaceOfSale('Магазин 2-й этаж')]
        self.places_of_sale[0].sale = self.sale

class Test_PlaceOfSale(TestPlaceOfSale):
    def test_initial(self):
        self.assertEqual(str(self.places_of_sale[0].sale.list_sli[0].item.product.name), "item1")

