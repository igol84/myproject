from unittest import TestCase

from prjstore.domain.seller import Seller


class TestSeller(TestCase):
    def setUp(self) -> None:
        self.sellers = {1: Seller('Igor'), 2: Seller('Anna'), 3: Seller('Sasha')}


class Test_Seller(TestSeller):
    def test_01_initial(self):
        self.assertEqual(str(self.sellers[1]), "Seller(name='Igor')")
        self.assertEqual(self.sellers[1].name, 'Igor')

    def test_02_edit_name(self):
        self.sellers[1].name = 'Anna'
        self.assertEqual(self.sellers[1].name, 'Anna')
