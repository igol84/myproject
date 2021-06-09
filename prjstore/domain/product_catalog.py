from dataclasses import field, asdict
from pprint import pprint

from pydantic import validate_arguments
from pydantic.dataclasses import dataclass

from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.products.shoes import Shoes
from util.money import Money


@dataclass
class ProductCatalog():
    """
>>> pc = get_products_for_test()  # create get test products
>>> d = asdict(pc[2])
>>> p = ProductFactory.create(**d)
>>> pc.set_product(ProductFactory.create(prod_id='7'))
>>> pc.set_product(ProductFactory.create(product_type='shoes', prod_id='8',\
 name='item12', price=(300, ), color='white',  size=40, length_of_insole=25.5))
>>> pc[2].name
'item23'
>>> pc.set_product(ProductFactory.create(prod_id='10', name='prod10', price=(500, )))
>>> pc['10'].name                                                   # get catalog
'prod10'
>>> pc.unset_product_by_pr_id('3')                       # del product by product id "7"
>>> del pc['10']
>>> list(pc.products.keys())                                                   # get catalog
['1', '2', '4', '6', '7', '8']
>>> print([product.name for product in pc.search(name='Item2').values()])  # search products by name containing "item"
['item23', 'item2']
    """
    products: dict[str, AbstractProduct] = field(init=False, default_factory=dict)

    ###############################################################################################
    @validate_arguments
    def set_product(self, pr: AbstractProduct) -> None:
        self.products[pr.prod_id] = pr

    @validate_arguments
    def unset_product_by_pr_id(self, pr_id: str) -> None:
        del self.products[pr_id]

    @validate_arguments
    def __delitem__(self, prod_id: str) -> None:
        self.unset_product_by_pr_id(prod_id)

    @validate_arguments
    def get_product_by_id(self, prod_id: str) -> AbstractProduct:
        if prod_id in self.products:
            return self.products[prod_id]
        raise IndexError(f"Invalid product id: {prod_id}")

    @validate_arguments
    def __getitem__(self, prod_id: str) -> AbstractProduct:
        return self.get_product_by_id(prod_id)

    @validate_arguments
    def search(self, name: str = None) -> dict[str, AbstractProduct]:
        products = {}
        if name:
            for product in self.products.values():
                if name.lower() in product.name.lower():
                    products[product.prod_id] = product
        return products


def get_products_for_test() -> ProductCatalog:
    pc = ProductCatalog()
    pc.set_product(ProductFactory.create(prod_id='1', product_type='shoes', name='item1', price=Money(100), size=36))
    pc.set_product(ProductFactory.create(prod_id='2', name='item23', price=Money(600)))
    pc.set_product(ProductFactory.create(prod_id='3', product_type='shoes', name='item4', price=Money(700), color='red',
                                         size=43.3, length_of_insole=28, width=Shoes.widths['Medium']))
    pc.set_product(ProductFactory.create(prod_id='4', name='item5', price=Money(300)))
    pc.set_product(ProductFactory.create(prod_id='6', name='item2', price=Money(500)))
    return pc
