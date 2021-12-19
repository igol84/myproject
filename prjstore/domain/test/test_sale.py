import datetime

import pytest

from prjstore.domain.sale import Sale
from prjstore.domain.seller import Seller
from prjstore.domain.test.test_item import TestItem


class TestSale:
    def setup(self) -> None:
        self.items = []
        TestItem.setup(self)
        self.sale = Sale(seller=Seller(1, 'Igor'))
        self.sale.add_line_item(self.items[1])
        self.sale.add_line_item(self.items[4], qty=2)
        self.sale.add_line_item(self.items[2], sale_price=200)
        self.sale.date_time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')


class Test_Sale(TestSale):
    def test_01_initial(self):
        sale = Sale(seller=Seller(1, 'Igor'))
        sale.date_time = datetime.datetime.strptime('6/6/20, 12:19:55', '%m/%d/%y, %H:%M:%S')
        assert str(sale.seller.name) == 'Igor'
        assert str(sale.list_sli) == '[]'
        assert str(sale.date_time) == '2020-06-06 12:19:55'

    def test_get_list_sli(self):
        list_sli = [(sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount) for sli in self.sale.list_sli]
        assert str(list_sli) == "[('item1', 0, 1, 100.0), ('item23', 1, 2, 600.0), ('item24', 1, 1, 200.0)]"

    def test_add_line_item(self):
        sli = [(sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount) for sli in self.sale[4]]
        assert str(sli) == "[('item23', 1, 2, 600.0)]"
        self.sale.add_line_item(self.items[4], sale_price=700)
        sli = [(sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount) for sli in self.sale[4]]
        assert str(sli) == "[('item23', 0, 2, 600.0), ('item23', 0, 1, 700.0)]"
        with pytest.raises(AssertionError):
            self.sale.add_line_item(self.items[4], sale_price=700)

    def test_add_line_item_2(self):
        self.sale.add_line_item(self.items[4], qty=1)
        sli = self.sale[(4, 600)]
        sli = [sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount]
        assert str(sli) == "['item23', 0, 3, 600.0]"

    def test_get_line_item_by_product_id(self):
        sli = self.sale.get_line_items_by('2', 600)[0]
        sli = [sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount]
        assert str(sli) == "['item23', 1, 2, 600.0]"

    def test_get_line_items_by_item_id(self):
        sli = self.sale.get_line_items_by_item_id(4)[0]
        sli = [sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount]
        assert str(sli) == "['item23', 1, 2, 600.0]"

    def test_get_line_item_by_item_id_and_sale_price(self):
        sli = self.sale.get_line_item_by_item_id_and_sale_price(4, 600)
        sli = [sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount]
        assert str(sli) == "['item23', 1, 2, 600.0]"

    def test_edit_sale_price(self):
        sli = self.sale.get_line_item_by_item_id_and_sale_price(4, 600)
        self.sale.edit_sale_price(sli=sli, new_sale_price=400)
        sli = [sli.item.product.name, sli.item.qty, sli.qty, sli.sale_price.amount]
        assert str(sli) == "['item23', 1, 2, 400.0]"

    def test_unset_line_item_by_pr_id(self):
        self.sale.unset_line_items_by_pr_id_and_sale_price('2', 600)
        assert self.sale[(4, 600)].qty == 1
        self.sale.unset_line_items_by_pr_id_and_sale_price('2', 600)
        assert self.sale[(4, 600)] == None

    def test_del_line_item_by_product_id(self):
        self.sale.del_line_items_by_product_id_and_sale_price('2', 600)
        assert self.sale.get_line_item_by_item_id_and_sale_price(4, 600) == None

    def test_del_line_item_by_product_id_2(self):
        del self.sale[(4, 600)]
        assert self.sale.get_line_items_by('2', 600) == []

    def test_del_line_items_by_item_id_and_sale_price(self):
        self.sale.del_line_items_by_item_id_and_sale_price(4, 600)
        assert self.sale.get_line_item_by_item_id_and_sale_price(4, 600) == None

    def test_is_complete(self):
        assert self.sale.is_complete() == False

    def test_completed(self):
        self.sale.completed()
        assert self.sale.is_complete() == True

    def test_get_time(self):
        assert str(self.sale.date_time) == '2020-06-06 12:19:55'

    def test_set_time(self):
        self.sale.date_time = datetime.datetime.strptime('6/6/20, 12:20:55', '%m/%d/%y, %H:%M:%S')
        assert str(self.sale.date_time) == '2020-06-06 12:20:55'

    def test_get_seller(self):
        assert str(self.sale.seller.name) == 'Igor'

    def test_set_seller(self):
        self.sale.seller = Seller(2, 'Anna')
        assert str(self.sale.seller.name) == 'Anna'

    def test_is_item_in_sale(self):
        assert self.sale.is_item_in_sale(self.items[3]) == False
        assert self.sale.is_item_in_sale(self.items[4]) == True

    def test_is_product_in_sale(self):
        assert self.sale.is_product_in_sale(self.items[3].product) == False
        assert self.sale.is_product_in_sale(self.items[4].product) == True

    def test_total(self):
        assert self.sale.get_total().amount == 1500.0

    def test_total_purchase(self):
        assert self.sale.get_total_purchase().amount == 490.5

    def test_total_profit(self):
        assert self.sale.get_total_profit().amount == 1009.5
