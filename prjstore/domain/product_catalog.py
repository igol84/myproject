from contracts import contract

from prjstore.domain.abstract_product import AbstractProduct
from prjstore.domain.product_factory import ProductFactory


class ProductCatalog(list):
    """
>>> pc = get_products_for_test()  # create get test products
>>> pc
[<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0, length_of_insole=11.0, width=Medium>,\
 <SimpleProduct: id=2, name=item23, price=UAH 600.00>,\
 <Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0, width=Medium>,\
 <SimpleProduct: id=4, name=item5, price=UAH 300.00>, <SimpleProduct: id=6, name=item2, price=UAH 500.00>]
>>> pc.quantity                                          # count of products
5
>>> pc.last_id                                           # get last id
'6'
>>> pc.new_id                                            # get new generated id  "last id + 1"
'7'
>>> pc.set_product(ProductFactory.create(product_id=pc.new_id))
>>> pc.set_product(ProductFactory.create(product_type='shoes', prod_id=pc.new_id,\
 name='item12', price=300, color='white',  size=40, length_of_insole=25.5))
>>> pc                                                   # get catalog
[<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0, length_of_insole=11.0, width=Medium>,\
 <SimpleProduct: id=2, name=item23, price=UAH 600.00>,\
 <Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0, width=Medium>,\
 <SimpleProduct: id=4, name=item5, price=UAH 300.00>,\
 <SimpleProduct: id=6, name=item2, price=UAH 500.00>, <SimpleProduct: id=7, name=item, price=UAH 0.00>,\
 <Shoes: id=8, name=item12, price=UAH 300.00, color=white, size=40.0, length_of_insole=25.5, width=Medium>]
>>> pc['2']                                              # get product by id='2'
<SimpleProduct: id=2, name=item23, price=UAH 600.00>
>>> pc.get_product_by_id('3')                            # get product by id='3'
<Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0, width=Medium>
>>> f_products = []
>>> for pr in pc:                               # get products, where price > 500 UAH
...     if pr.price.UAH.amount > 500 :
...         f_products.append((pr.name, pr.price.USD))
>>> f_products
[('item23', USD 21.82), ('item4', USD 25.45)]
>>> pc.set_product(ProductFactory.create(product_id=pc.new_id, name='prod', price=500))
>>> pc                                                   # get catalog
[<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0, length_of_insole=11.0, width=Medium>,\
 <SimpleProduct: id=2, name=item23, price=UAH 600.00>,\
 <Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0, width=Medium>,\
 <SimpleProduct: id=4, name=item5, price=UAH 300.00>, <SimpleProduct: id=6, name=item2, price=UAH 500.00>,\
 <SimpleProduct: id=7, name=item, price=UAH 0.00>,\
 <Shoes: id=8, name=item12, price=UAH 300.00, color=white, size=40.0, length_of_insole=25.5, width=Medium>,\
 <SimpleProduct: id=9, name=prod, price=UAH 500.00>]
>>> pc.unset_product_by_pr_id('3')                       # del product by product id "7"
>>> del pc['7']
>>> pc                                                   # get catalog
[<Shoes: id=1, name=item1, price=UAH 100.00, color=default, size=36.0, length_of_insole=11.0, width=Medium>,\
 <SimpleProduct: id=2, name=item23, price=UAH 600.00>, <SimpleProduct: id=4, name=item5, price=UAH 300.00>,\
 <SimpleProduct: id=6, name=item2, price=UAH 500.00>,\
 <Shoes: id=8, name=item12, price=UAH 300.00, color=white, size=40.0, length_of_insole=25.5, width=Medium>,\
 <SimpleProduct: id=9, name=prod, price=UAH 500.00>]
>>> pc.search(name='Item2')                               # search products by name containing "item"
[<SimpleProduct: id=2, name=item23, price=UAH 600.00>,\
 <SimpleProduct: id=6, name=item2, price=UAH 500.00>\
]
    """

    def __init__(self):
        super().__init__()

    ###############################################################################################
    # quantity
    def quantity(self) -> int:
        return len(self)

    quantity = property(quantity)

    ###############################################################################################
    # last_id
    def __last_id(self) -> str:
        return str(sorted([int(pr.id) for pr in self])[-1])

    last_id = property(__last_id)

    ###############################################################################################
    # new_id
    def __new_id(self) -> str:
        return str(int(self.last_id) + 1)

    new_id = property(__new_id)

    ###############################################################################################
    @contract(pr=AbstractProduct)
    def set_product(self, pr: AbstractProduct) -> None:
        self.append(pr)

    @contract(pr_id=str)
    def unset_product_by_pr_id(self, pr_id: str) -> None:
        self.remove(self[pr_id])

    def __delitem__(self, prod_id: str) -> None:
        self.unset_product_by_pr_id(prod_id)

    def get_product_by_id(self, prod_id: str) -> AbstractProduct:
        for pr in self:
            if pr.id == prod_id:
                return pr
        raise IndexError(f"Invalid product id: {prod_id}")

    def __getitem__(self, prod_id: str) -> AbstractProduct:
        return self.get_product_by_id(prod_id)

    def search(self, name: str = None) -> list[AbstractProduct]:
        products = []
        if name:
            for product in self:
                if name.lower() in product.name.lower():
                    products.append(product)
        return products


def get_products_for_test() -> ProductCatalog:
    pc = ProductCatalog()
    pc.set_product(ProductFactory.create(product_type='shoes', prod_id='1', name='item1', price=100, size=36))
    pc.set_product(ProductFactory.create(product_id='2', name='item23', price=600))
    pc.set_product(ProductFactory.create(product_type='shoes', prod_id='3', name='item4', price=700, color='red',
                                         size=43.3, length_of_insole=28))
    pc.set_product(ProductFactory.create(product_id='4', name='item5', price=300))
    pc.set_product(ProductFactory.create(product_id='6', name='item2', price=500))
    return pc
