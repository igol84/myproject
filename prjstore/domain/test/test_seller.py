from unittest import TestCase

from prjstore.domain.seller import Seller


class TestSeller(TestCase):
    def setUp(self) -> None:
        self.sellers = [Seller('Igor'), Seller('Anna'), Seller('Sasha')]

class Test_Seller(TestSeller):
    def test_01_initial(self):
        self.assertEqual(str(self.sellers[0]), '<Seller: name=Igor>')
        self.assertEqual(self.sellers[0].name, 'Igor')

    def test_02_edit_name(self):
        self.sellers[0].name = 'Anna'
        self.assertEqual(self.sellers[0].name, 'Anna')
