from unittest import TestCase
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import widths
from util.money import Money


class TestShoes(TestCase):
    def setUp(self) -> None:
        self.shoes = ProductFactory.create(product_type='shoes', prod_id='6', name='nike air force', price=Money(900),
                                           color='red', size=43, length_of_insole=28.5, width=widths['Wide'])

class Test_Shoes(TestShoes):
    def test_01_initial(self):
        self.assertEqual(str(self.shoes),
        "Shoes(prod_id='6', name='nike air force', price=Money(amount=900.0, "
        "currency=Currency(code='UAH', rate=27.5, sign='₴')), color='red', size=43.0, length_of_insole=28.5, "
        "width=Width(name='Wide', short_name='EE'))")
        self.assertEqual(self.shoes.color, 'red')
        self.assertEqual(self.shoes.size, 43.0)
        self.assertEqual(self.shoes.length_of_insole, 28.5)
        self.assertEqual(str(self.shoes.width.name), 'Wide')

    def test_02_initial(self):
        self.shoes = ProductFactory.create(product_type='shoes', prod_id='02')
        self.assertEqual(str(self.shoes.name), 'item')

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
        self.shoes.width = widths['Extra Wide']
        self.assertEqual(str(self.shoes.width.name), 'Extra Wide')
        self.assertEqual(self.shoes.width.short_name, '4E')

    def test_03_edit(self):
        self.shoes.edit(color='black', size=44.5, length_of_insole=28.5, width='Medium')
        self.assertEqual(str(self.shoes.color), 'black')
        self.assertEqual(str(self.shoes.size), '44.5')
        self.assertEqual(str(self.shoes.length_of_insole), '28.5')
        self.assertEqual(str(self.shoes.width.name), 'Medium')
