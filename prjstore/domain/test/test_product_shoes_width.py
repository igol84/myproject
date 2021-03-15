from unittest import TestCase
from prjstore.domain.products.shoes_components import Width

class TestShoesWidth(TestCase):
    def setUp(self) -> None:
        self.width = Width(name='Wide', short_name='EE')

class Test_ShoesWidth(TestShoesWidth):
    def test_01_initial(self):
        self.assertEqual(str(self.width), 'Wide')
        self.assertEqual(self.width.short_name, 'EE')

    def test_02_edit_color(self):
        self.width.name = 'Extra Wide'
        self.assertEqual(str(self.width), 'Extra Wide')

    def test_02_edit_short_name(self):
        self.width.short_name = '4E'
        self.assertEqual(str(self.width.short_name), '4E')

    def test_03_contract_raises(self):
        self.assertRaises(TypeError, Width, name='Wide')
        self.assertRaises(TypeError, Width, short_name='EE')
