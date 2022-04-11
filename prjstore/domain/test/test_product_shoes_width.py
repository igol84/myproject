import pytest

from prjstore.domain.products.shoes_components import Width


class TestShoesWidth:
    def setup(self) -> None:
        self.width = Width(name='Wide', short_name='EE', width_of_insole=11)


class Test_ShoesWidth(TestShoesWidth):
    def test_01_initial(self):
        assert str(self.width.name) == 'Wide'
        assert self.width.short_name == 'EE'
        assert self.width.width_of_insole == 11

    def test_02_edit_color(self):
        self.width.name = 'Extra Wide'
        assert str(self.width.name) == 'Extra Wide'

    def test_02_edit_short_name(self):
        self.width.short_name = '4E'
        assert str(self.width.short_name) == '4E'

    def test_03_contract_raises(self):
        with pytest.raises(TypeError):
            Width(name='Wide')
        with pytest.raises(TypeError):
            Width(short_name='EE')
