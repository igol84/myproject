from unittest import TestCase

from prjstore.domain.seller import Seller


class TestSeller(TestCase):
    def setUp(self) -> None:
        self.sellers = {1: Seller(1, 'Igor'), 2: Seller(2, 'Anna'), 3: Seller(3, 'Sasha')}


class Test_Seller(TestSeller):
    def test_01_initial(self):
        self.assertEqual(self.sellers[1].name, 'Igor')

    def test_02_edit_name(self):
        self.sellers[1].name = 'Anna'
        self.assertEqual(self.sellers[1].name, 'Anna')
