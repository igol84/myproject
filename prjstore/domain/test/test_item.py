from datetime import date

from prjstore.domain.item import Item
from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from util.money import Money


class TestItem:

    def setup(self) -> None:
        self.pc = ProductCatalog()
        TestProductCatalog.setup(self)
        self.items = {
            1: Item(id=1, product=self.pc.products['1'], buy_price=(40,), date_buy=date.today()),
            2: Item(id=2, product=self.pc.products['3'], buy_price=(50.5,), qty=2),
            3: Item(id=3, product=self.pc.products['6'], buy_price=(100.5,)),
            4: Item(id=4, product=self.pc.products['2'], qty=3, buy_price=(200,)),
            5: Item(id=5, product=self.pc.products['2'], qty=3, buy_price=(300,)),
        }


class Test_Item(TestItem):
    def test_01_initial(self):
        assert str(self.items[4].product.name) == 'item23'
        assert str(self.items[4].qty) == '3'
        assert str(self.items[4].buy_price.amount) == '200.0'

    def test_02_edit(self):
        self.items[4].product = self.pc['3']
        assert str(self.items[4].product.name) == 'item24'
        assert str(self.items[4].qty) == '3'
        assert str(self.items[4].buy_price.amount) == '200.0'

    def test_03_edit_qty(self):
        self.items[1].qty = 1
        assert self.items[1].qty == 1

    def test_04_edit_price(self):
        assert str(self.items[1].buy_price.amount) == '40.0'
        self.items[1].buy_price = Money(200)
        assert str(self.items[1].buy_price.amount) == '200.0'
