from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from util.money import Money


class TestShoes:
    def setup(self) -> None:
        self.shoes = ProductFactory.create(product_type='shoes', prod_id='6', name='nike air force', price=Money(900),
                                           color='red', size=43, length_of_insole=28.5, width=Shoes.widths['Wide'])


class Test_Shoes(TestShoes):
    def test_01_initial(self):
        assert str(self.shoes.name) == 'nike air force'
        assert self.shoes.color == 'red'
        assert self.shoes.size == 43.0
        assert self.shoes.length_of_insole == 28.5
        assert str(self.shoes.width.name) == 'Wide'

    def test_02_initial(self):
        self.shoes = ProductFactory.create(product_type='shoes', prod_id='02')
        assert str(self.shoes.name) == 'item'

    def test_02_edit_color(self):
        self.shoes.color = 'white'
        assert self.shoes.color == 'white'

    def test_02_edit_size(self):
        self.shoes.size = 43.3
        assert self.shoes.size == 43.3

    def test_02_edit_length_of_insole(self):
        self.shoes.length_of_insole = 29
        assert self.shoes.length_of_insole == 29

    def test_02_edit_width(self):
        self.shoes.width = Shoes.widths['Extra Wide']
        assert str(self.shoes.width.name) == 'Extra Wide'
        assert self.shoes.width.short_name == '4E'

    def test_03_edit(self):
        self.shoes.edit(color='black', size=44.5, length_of_insole=28.5, width='Medium')
        assert str(self.shoes.color) == 'black'
        assert str(self.shoes.size) == '44.5'
        assert str(self.shoes.length_of_insole) == '28.5'
        assert str(self.shoes.width.name) == 'Medium'

    def test_04_clone(self):
        clone_shoes = self.shoes.copy(prod_id='111')
        assert clone_shoes != self.shoes
        assert clone_shoes.prod_id != self.shoes.prod_id
        assert clone_shoes.name == self.shoes.name
        assert clone_shoes.price == self.shoes.price
        assert clone_shoes.product_type == self.shoes.product_type
        assert clone_shoes.color == self.shoes.color
        assert clone_shoes.size == self.shoes.size
        clone_shoes.size = 46
        assert clone_shoes.size != self.shoes.size
        assert clone_shoes.length_of_insole == self.shoes.length_of_insole
        assert clone_shoes.width == self.shoes.width
