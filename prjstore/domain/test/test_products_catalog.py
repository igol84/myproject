from unittest import TestCase

from prjstore.domain.product_catalog import ProductCatalog
from prjstore.domain.product_factory import ProductFactory


class TestProductCatalog(TestCase):

    def setUp(self) -> None:
        self.pc = ProductCatalog()
        self.pc.set_product(ProductFactory.create(product_type='shoes', prod_id='1', name='item1', price=100, size=36))
        self.pc.set_product(ProductFactory.create(id='2', name='item23', price=600))
        self.pc.set_product(ProductFactory.create(product_type='shoes', prod_id='3', name='item24', price=700,
                                                  color='red', size=43.3, length_of_insole=28))
        self.pc.set_product(ProductFactory.create(id='4', name='item5', price=300))
        self.pc.set_product(ProductFactory.create(id='6', name='item2', price=500))

class Test_ProductCatalog(TestProductCatalog):
    def test_01_initial(self):
        self.assertEqual(str(self.pc),
                         '[<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0, length_of_insole=11.0,'
                         ' width=Medium>,'
                         ' <SimpleProduct: id=2, name=item23, price=UAH 600.00>,'
                         ' <Shoes: id=3, name=item24, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0,'
                         ' width=Medium>,'
                         ' <SimpleProduct: id=4, name=item5, price=UAH 300.00>,'
                         ' <SimpleProduct: id=6, name=item2, price=UAH 500.00>]')

    def test_02_unset_product_by_pr_id(self):
        self.pc.unset_product_by_pr_id('3')
        self.assertEqual(str(self.pc),
                         '[<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0, length_of_insole=11.0,'
                         ' width=Medium>,'
                         ' <SimpleProduct: id=2, name=item23, price=UAH 600.00>,'
                         ' <SimpleProduct: id=4, name=item5, price=UAH 300.00>,'
                         ' <SimpleProduct: id=6, name=item2, price=UAH 500.00>]')

    def test_03_get_product_by_id(self):
        self.assertEqual(str(self.pc['2']), '<SimpleProduct: id=2, name=item23, price=UAH 600.00>')
        self.assertEqual(str(self.pc.get_product_by_id('3')),
                         '<Shoes: id=3, name=item24, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0,'
                         ' width=Medium>')

    def test_04_search(self):
        pr_list = self.pc.search(name='Item2')
        self.assertEqual(str(pr_list),
                         '[<SimpleProduct: id=2, name=item23, price=UAH 600.00>,'
                         ' <Shoes: id=3, name=item24, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0,'
                         ' width=Medium>,'
                         ' <SimpleProduct: id=6, name=item2, price=UAH 500.00>]')

    def test_05_quantity(self):
        self.assertEqual(self.pc.quantity, 5)

    def test_06_last_id(self):
        self.assertEqual(self.pc.last_id, '6')

    def test_07_new_id(self):
        self.assertEqual(self.pc.new_id, '7')
