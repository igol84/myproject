from unittest import TestCase
from prjstore.domain.product_factory import ProductFactory


class TestShoes(TestCase):
    def setUp(self) -> None:
        self.shoes = ProductFactory.create(product_type='shoes', prod_id='6', name='nike air force', price=900,
                                           color='red', size=43, length_of_insole=28.5, width='Wide')

class Test_Shoes(TestShoes):
    def test_01_initial(self):
        self.assertEqual(str(self.shoes),
                         '<Shoes: id=6, name=nike air force, price=UAH 900.00, color=red, size=43.0, '
                         'length_of_insole=28.5, width=Wide>')
        self.assertEqual(self.shoes.color, 'red')
        self.assertEqual(self.shoes.size, 43.0)
        self.assertEqual(self.shoes.length_of_insole, 28.5)
        self.assertEqual(str(self.shoes.width), 'Wide')

    def test_02_initial(self):
        self.shoes = ProductFactory.create(product_type='shoes', prod_id='02')
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
        self.assertEqual(str(self.shoes.width), 'Extra Wide')
        self.assertEqual(self.shoes.width.short_name, '4E')

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
