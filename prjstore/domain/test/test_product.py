from unittest import TestCase
from util.money import Money
from prjstore.domain.product_factory import ProductFactory


class TestSimpleProduct(TestCase):
    def setUp(self) -> None:
        self.simple_product = ProductFactory.create(prod_id='01', name='product1', price=Money(amount=25))

class Test_SimpleProduct(TestSimpleProduct):
    def test_01_initial(self):
        self.assertEqual(self.simple_product.prod_id, '01')
        self.assertEqual(self.simple_product.name, 'product1')
        self.assertEqual(str(self.simple_product.price.format()), '25.00₴')

    def test_01a_initial(self):
        self.simple_product = ProductFactory.create(product_type='product', prod_id='02')
        self.assertEqual(str(self.simple_product.name), 'item')

    def test_02_edit_name(self):
        self.simple_product.name = 'product2'
        self.assertEqual(self.simple_product.name, 'product2')

    def test_02_edit_price(self):
        self.simple_product.price = Money(550)
        self.assertEqual(str(self.simple_product.price.amount), '550.0')
        self.simple_product.convert_price('USD')
        self.assertEqual(str(self.simple_product.price.amount), '20.0')


    def test_03_edit(self):
        self.simple_product.edit(name='product3', price=Money(28, Money.currencies['USD']))
        self.assertEqual(str(self.simple_product.name), 'product3')
        self.assertEqual(str(self.simple_product.price.amount), '28.0')
        self.simple_product.edit(name='product4')
        self.assertEqual(str(self.simple_product.name), 'product4')
        self.simple_product.edit(price=29.5)
        self.assertEqual(str(self.simple_product.price.amount), '29.0')
        self.simple_product.edit(currency='UAH')
        self.assertEqual(str(self.simple_product.price.currency.code), 'UAH')
