from util.money import Money
from prjstore.domain.product_factory import ProductFactory


class TestSimpleProduct:
    def setup(self) -> None:
        self.simple_product = ProductFactory.create(prod_id='01', name='product1', price=Money(amount=25))


class Test_SimpleProduct(TestSimpleProduct):
    def test_01_initial(self):
        assert self.simple_product.prod_id == '01'
        assert self.simple_product.name == 'product1'
        assert self.simple_product.price.format() == '25.00₴'

    def test_01a_initial(self):
        self.simple_product = ProductFactory.create(product_type='product', prod_id='02')
        assert str(self.simple_product.name) == 'item'

    def test_02_edit_name(self):
        self.simple_product.name = 'product2'
        assert self.simple_product.name == 'product2'

    def test_02_edit_price(self):
        self.simple_product.price = Money(550)
        assert str(self.simple_product.price.amount) == '550.0'
        self.simple_product.convert_price('USD')
        assert str(self.simple_product.price.amount) == '20.0'

    def test_03_edit(self):
        self.simple_product.edit(name='product3', price=Money(28, Money.currencies['USD']))
        assert str(self.simple_product.name) == 'product3'
        assert str(self.simple_product.price.amount) == '28.0'
        self.simple_product.edit(name='product4')
        assert str(self.simple_product.name) == 'product4'
        self.simple_product.edit(price=29.5)
        assert str(self.simple_product.price.amount) == '29.0'
        self.simple_product.edit(currency='UAH')
        assert str(self.simple_product.price.currency.code) == 'UAH'

    def test_04_clone(self):
        clone_product = self.simple_product.copy()
        assert clone_product.prod_id != self.simple_product.prod_id
        assert clone_product.name == self.simple_product.name
        assert clone_product.price == self.simple_product.price
        assert clone_product.product_type == self.simple_product.product_type
