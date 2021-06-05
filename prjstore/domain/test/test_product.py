from unittest import TestCase
from util.money_my import Money, Decimal
from prjstore.domain.product_factory import ProductFactory


class TestSimpleProduct(TestCase):
    def setUp(self) -> None:
        self.simple_product = ProductFactory.create(product_id='01', name='product1', price=25, currency='UAH')

class Test_SimpleProduct(TestSimpleProduct):
    def test_01_initial(self):
        self.assertEqual(str(self.simple_product), '<SimpleProduct: id=01, name=product1, price=UAH 25.00>')
        self.assertEqual(self.simple_product.id, '01')
        self.assertEqual(self.simple_product.name, 'product1')
        self.assertEqual(str(self.simple_product.price), 'UAH 25.00')

    def test_01a_initial(self):
        self.simple_product = ProductFactory.create(product_type='product', product_id='02')
        self.assertEqual(str(self.simple_product), '<SimpleProduct: id=02, name=item, price=UAH 0.00>')

    def test_02_edit_name(self):
        self.simple_product.name = 'product2'
        self.assertEqual(self.simple_product.name, 'product2')

    def test_02_edit_price(self):
        self.simple_product.price = 550
        self.assertEqual(str(self.simple_product.price), 'UAH 550.00')
        self.simple_product.price = 650.50
        self.assertEqual(str(self.simple_product.price), 'UAH 650.50')
        self.simple_product.price = Decimal(750.50)
        self.assertEqual(str(self.simple_product.price), 'UAH 750.50')
        self.simple_product.convert_price('USD')
        self.assertEqual(str(self.simple_product.price), 'USD 27.29')
        self.simple_product.price = Money(27)
        self.assertEqual(str(self.simple_product.price), 'UAH 27.00')

    def test_03_edit(self):
        self.simple_product.edit(name='product3', price=28, currency='USD')
        self.assertEqual(str(self.simple_product), '<SimpleProduct: id=01, name=product3, price=USD 28.00>')
        self.simple_product.edit(name='product4')
        self.assertEqual(str(self.simple_product), '<SimpleProduct: id=01, name=product4, price=USD 28.00>')
        self.simple_product.edit(price=29.5)
        self.assertEqual(str(self.simple_product), '<SimpleProduct: id=01, name=product4, price=USD 29.50>')
        self.simple_product.edit(currency='UAH')
        self.assertEqual(str(self.simple_product), '<SimpleProduct: id=01, name=product4, price=UAH 29.50>')
