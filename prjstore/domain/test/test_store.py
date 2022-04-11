import pytest

from prjstore.domain.store import Store
from prjstore.domain.test.test_item import TestItem
from prjstore.domain.test.test_place_of_sale import TestPlaceOfSale
from prjstore.domain.test.test_products_catalog import TestProductCatalog
from prjstore.domain.test.test_seller import TestSeller


class TestStore:
    def setup(self) -> None:
        self.store = Store(id=1, name='Giga')
        self.pc = None
        TestProductCatalog.setup(self)
        self.store.pc = self.pc
        self.items = {}
        TestItem.setup(self)
        self.store.items = self.items
        self.sellers = []
        TestSeller.setup(self)
        self.store.sellers = self.sellers
        self.places_of_sale = []
        TestPlaceOfSale.setup(self)
        self.store.places_of_sale = self.places_of_sale


class Test_Store(TestStore):
    def test_01_pc(self):
        assert len(self.store.pc.products) == 5
        assert self.store.pc['1'].name == 'item1'

    def test_02_items(self):
        assert len(self.store.items) == 5
        assert self.store.items[4].product.name == 'item23'

    def test_03_sellers(self):
        assert len(self.store.sellers) == 3
        assert self.store.sellers[3].name == 'Sasha'

    def test_04_places_of_sale(self):
        assert len(self.store.places_of_sale) == 4
        assert str(self.store.places_of_sale[1].sale.list_sli[0].item.product.name) == 'item1'

    def test_04_get_item_by_pr_id(self):
        assert self.store.get_items_by_pr_id('2')[0].product.name == 'item23'

    def test_05_search_item(self):
        assert len(self.store.search_items(value='item2', fields={'name'})) == 4

    def test_06_move_sale_to_another_place(self):
        sale = self.store.places_of_sale[1].sale
        self.store.places_of_sale[1].sale = None
        self.store.places_of_sale[1].sale = sale
        assert self.store.places_of_sale[2].sale == None
        assert len(self.store.places_of_sale[1].sale) == 3

    def test_07_add_item(self):
        item = self.store.items[1]
        assert str([item.product.name, item.qty, item.buy_price.amount]) == "['item1', 1, 40.0]"
        self.store.add_item(item=item, qty=5)
        assert item.qty == 6

    def test_08_add_new_item(self):
        item = self.store.items[1]
        item.qty = 0
        del self.store.items[1]
        assert item.qty == 0
        with pytest.raises(IndexError):
            self.store.get_items_by_pr_id(pr_id=item.product.prod_id)
        self.store.add_item(item=item, qty=5)
        assert item.qty == 5

    def test_09_update_sale_price(self):
        sli = self.store.places_of_sale[1].sale.list_sli[1]
        assert str([sli.item.product.prod_id, sli.item.qty, sli.qty, sli.sale_price.amount]) == "['2', 1, 2, 600.0]"
        self.store.places_of_sale[1].sale.add_line_item(sli.item, 50)
        sli = self.store.places_of_sale[1].sale.list_sli[1]
        assert str([sli.item.product.prod_id, sli.item.qty, sli.qty, sli.sale_price.amount]) == "['2', 0, 2, 600.0]"
        new_sli = self.store.places_of_sale[1].sale[(4, 50)]
        assert str([new_sli.item.product.prod_id, new_sli.item.qty, new_sli.qty,
                    new_sli.sale_price.amount]) == "['2', 0, 1, 50.0]"
        self.store.places_of_sale[1].sale.edit_sale_price(sli, 50)
        assert str([new_sli.item.product.prod_id, new_sli.item.qty, new_sli.qty,
                    new_sli.sale_price.amount]) == "['2', 0, 3, 50.0]"
        assert self.store.places_of_sale[1].sale[(4, 600)] == None
