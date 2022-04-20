from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.test.test_sale import TestSale
from prjstore.domain.test.test_expense import TestExpense
from util.money import Money


class TestPlaceOfSale:
    def setup(self) -> None:
        self.items = []
        self.sale = None
        TestSale.setup(self)

        self.places_of_sale = {1: PlaceOfSale(1, 'Интернет'), 2: PlaceOfSale(2, 'Бокс 47'),
                               3: PlaceOfSale(3, 'Магазин 1-й этаж'), 4: PlaceOfSale(4, 'Магазин 2-й этаж')}
        self.places_of_sale[1].sale = self.sale
        test_sale = TestSale()
        test_sale.setup_ledger(self.places_of_sale[1])
        TestExpense.setup(self.places_of_sale[1])


class Test_PlaceOfSale(TestPlaceOfSale):
    def test_initial(self):
        assert str(self.places_of_sale[1].sale.list_sli[0].item.product.name) == "item1"

    def test_report(self):
        assert self.places_of_sale[1].get_monthly_report()[(2, 2022)] == Money(909.0)
