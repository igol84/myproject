from unittest import TestCase

from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.product_factory import ProductFactory


class TestProductCatalog(TestCase):

    def setUp(self) -> None:
        self.pc = ProductCatalog()
        self.pc.set_product(ProductFactory.create(product_type='shoes', prod_id='1', name='item1', price=(100,),
                                                  size=36))
        self.pc.set_product(ProductFactory.create(prod_id='2', name='item23', price=(600,)))
        self.pc.set_product(ProductFactory.create(product_type='shoes', prod_id='3', name='item24', price=(700,),
                                                  color='red', size=43.3, length_of_insole=28))
        self.pc.set_product(ProductFactory.create(prod_id='4', name='item5', price=(300,)))
        self.pc.set_product(ProductFactory.create(prod_id='6', name='item2', price=(500,)))


class Test_ProductCatalog(TestProductCatalog):
    def test_01_initial(self):
        self.assertEqual(str([pr.name for pr in self.pc.products.values()]),
                         "['item1', 'item23', 'item24', 'item5', 'item2']")

    def test_02_1_unset_product_by_pr_id(self):
        self.pc.unset_product_by_pr_id('3')
        self.assertEqual(str([pr.name for pr in self.pc.products.values()]),
                         "['item1', 'item23', 'item5', 'item2']")

    def test_02_2_unset_product_by_pr_id(self):
        del self.pc['3']
        self.assertEqual(str([pr.name for pr in self.pc.products.values()]),
                         "['item1', 'item23', 'item5', 'item2']")

    def test_03_get_product_by_id(self):
        self.assertEqual(str(self.pc.products['2'].name), 'item23')
        self.assertEqual(str(self.pc.get_product_by_id('3').name), 'item24')

    def test_04_search(self):
        pr_list = self.pc.search(name='Item2')
        self.assertEqual(str([product.name for product in pr_list.values()]),
                         "['item23', 'item24', 'item2']")
