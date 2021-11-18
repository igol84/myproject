from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.products.simple_product import SimpleProduct


class TestProductFactory:
    def test_create_simple_product(self):
        self.product = ProductFactory.create(product_type='product', prod_id='01', name='product1', price=(25,))
        assert isinstance(self.product, SimpleProduct)
        self.product = ProductFactory.create(prod_id='01', name='product1', price=(25,))
        assert isinstance(self.product, SimpleProduct)


class Test_ProductFactory(TestProductFactory):
    def test_create_shoes(self):
        self.product = ProductFactory.create(product_type='shoes', prod_id='6', name='nike air force', price=(900,),
                                             color='red', size=43, length_of_insole=28.5, width=Shoes.widths['Wide'])
        assert isinstance(self.product, Shoes)
