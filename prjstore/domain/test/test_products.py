from unittest import TestCase
from util.money_my import MoneyMy, Decimal
from prjstore.domain.products import *


class TestSimpleProduct(TestCase):
    def setUp(self) -> None:
        self.simple_product = SimpleProduct(id='01', name='product1', price=25, currency='UAH')

    def test_01_initial(self):
        self.assertEqual(str(self.simple_product), '<SimpleProduct: id=01, name=product1, price=UAH 25.00>')
        self.assertEqual(self.simple_product.id, '01')
        self.assertEqual(self.simple_product.name, 'product1')
        self.assertEqual(str(self.simple_product.price), 'UAH 25.00')

    def test_01a_initial(self):
        self.simple_product = SimpleProduct(id='02')
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
        self.simple_product.price = MoneyMy(27)
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


class TestShoes(TestCase):
    def setUp(self) -> None:
        self.shoes = Shoes(prod_id='6', name='nike air force', price=900, color='red', size=43, length_of_insole=28.5,
                           width='Wide')

    def test_01_initial(self):
        self.assertEqual(str(self.shoes),
                         '<Shoes: id=6, name=nike air force, price=UAH 900.00, color=red, size=43.0, '
                         'length_of_insole=28.5, width=Wide>')
        self.assertEqual(self.shoes.color, 'red')
        self.assertEqual(self.shoes.size, 43.0)
        self.assertEqual(self.shoes.length_of_insole, 28.5)
        self.assertEqual(self.shoes.width, 'Wide')

    def test_02_initial(self):
        self.shoes = Shoes(prod_id='02')
        self.assertEqual(str(self.shoes), '<Shoes: id=02, name=item, price=UAH 0.00, color=default, size=1.0, '
                                          'length_of_insole=11.0, width=Medium>')

    def test_02_edit_color(self):
        self.shoes.color = 'white'
        self.assertEqual(self.shoes.color, 'white')

    def test_02_edit_size(self):
        self.shoes.size = 43.3
        self.assertEqual(self.shoes.size, 43.3)

    def test_02_edit_length_of_insole(self):
        self.shoes.length_of_insole = 29
        self.assertEqual(self.shoes.length_of_insole, 29)

    def test_02_edit_width(self):
        self.shoes.width = 'Extra Wide'
        self.assertEqual(self.shoes.width, 'Extra Wide')

    def test_03_edit(self):
        self.shoes.edit(color='black', size=44.5, length_of_insole=28.5, width='Medium')
        self.assertEqual(str(self.shoes),
                         '<Shoes: id=6, name=nike air force, price=UAH 900.00, color=black, size=44.5, '
                         'length_of_insole=28.5, width=Medium>')
        self.shoes.edit(color='pink')
        self.assertEqual(str(self.shoes),
                         '<Shoes: id=6, name=nike air force, price=UAH 900.00, color=pink, size=44.5, '
                         'length_of_insole=28.5, width=Medium>')
        self.shoes.edit(size='45')
        self.assertEqual(str(self.shoes),
                         '<Shoes: id=6, name=nike air force, price=UAH 900.00, color=pink, size=45.0, '
                         'length_of_insole=28.5, width=Medium>')
        self.shoes.edit(length_of_insole='29')
        self.assertEqual(str(self.shoes),
                         '<Shoes: id=6, name=nike air force, price=UAH 900.00, color=pink, size=45.0, '
                         'length_of_insole=29.0, width=Medium>')
        self.shoes.edit(width='Extra Wide')
        self.assertEqual(str(self.shoes),
                         '<Shoes: id=6, name=nike air force, price=UAH 900.00, color=pink, size=45.0, '
                         'length_of_insole=29.0, width=Extra Wide>')
