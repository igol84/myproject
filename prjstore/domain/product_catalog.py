from product_desc import *


class ProductCatalog(dict):
    """
    >>> pc = ProductCatalog()                                # create catalog, and add there a products
    >>> pc.set_product(ProductDesc())
    >>> pc.set_product(ProductDesc(desc='item2', price=300))
    >>> pc                              # get products
    {'1': <Product: id=1, desc=item, price=UAH 0.00>, '2': <Product: id=2, desc=item2, price=UAH 300.00>}
    >>> pc['2']                                              # get product with id='2'
    <Product: id=2, desc=item2, price=UAH 300.00>
    >>> pc.set_product(ProductDesc(desc='prod', price=500))
    >>> pc.search(desc='item')                               # search products whose name contains "item"
    [<Product: id=1, desc=item, price=UAH 0.00>, <Product: id=2, desc=item2, price=UAH 300.00>]
    >>> pc.count()                                           # count of products
    3


    """

    def set_product(self, pr):
        dict.__setitem__(self, pr.id, pr)

    def search (self, desc=None):
        if desc:
            products=[]
            for key, product in self.items():
                if desc in product.desc:
                    products.append(self[key])
            return products
        return False

    def count(self):
        return len(self)

