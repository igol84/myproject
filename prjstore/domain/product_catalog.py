from product_desc import *


class ProductCatalog(dict):
    """
>>> pc = ProductCatalog().get_products_for_test()  # create get test products
>>> pc                         #
{'1': <Product: id=1, desc=item1, price=UAH 100.00>, '6': <Product: id=6, desc=item2, price=UAH 500.00>,\
 '2': <Product: id=2, desc=item23, price=UAH 600.00>, '3': <Product: id=3, desc=item4, price=UAH 700.00>,\
 '4': <Product: id=4, desc=item5, price=UAH 300.00>}
>>> pc.last_id                                           # get last id
6
>>> pc.new_id                                            # get new generated id  "last id + 1"
'7'
>>> pc.set_product(ProductDesc(item_id=pc.new_id))
>>> pc.set_product(ProductDesc(item_id=pc.new_id, desc='item12', price=300))
>>> pc                                                   # get catalog
{'1': <Product: id=1, desc=item1, price=UAH 100.00>, '6': <Product: id=6, desc=item2, price=UAH 500.00>, \
'2': <Product: id=2, desc=item23, price=UAH 600.00>, '3': <Product: id=3, desc=item4, price=UAH 700.00>, \
'4': <Product: id=4, desc=item5, price=UAH 300.00>, '7': <Product: id=7, desc=item, price=UAH 0.00>, \
'8': <Product: id=8, desc=item12, price=UAH 300.00>}
>>> pc['2']                                              # get product by id='2'
<Product: id=2, desc=item23, price=UAH 600.00>
>>> pc.set_product(ProductDesc(item_id=pc.new_id, desc='prod', price=500))
>>> pc.search(desc='item2')                               # search products by name containing "item"
[<Product: id=6, desc=item2, price=UAH 500.00>, <Product: id=2, desc=item23, price=UAH 600.00>]
>>> pc.count                                           # count of products
8
>>> pc                                                   # get catalog
{'1': <Product: id=1, desc=item1, price=UAH 100.00>, '6': <Product: id=6, desc=item2, price=UAH 500.00>, \
'2': <Product: id=2, desc=item23, price=UAH 600.00>, '3': <Product: id=3, desc=item4, price=UAH 700.00>, \
'4': <Product: id=4, desc=item5, price=UAH 300.00>, '7': <Product: id=7, desc=item, price=UAH 0.00>, \
'8': <Product: id=8, desc=item12, price=UAH 300.00>, '9': <Product: id=9, desc=prod, price=UAH 500.00>}



    """

    def __init__(self):
        super().__init__()


    def set_product(self, pr):
        dict.__setitem__(self, pr.id, pr)

    def search(self, desc=None):
        if desc:
            products = []
            for key, product in self.items():
                if desc in product.desc:
                    products.append(self[key])
            return products
        return False

    def count(self):
        return len(self)

    count = property(count)

    def last_id(self):
        return sorted([int(key) for key in self])[-1]

    last_id = property(last_id)

    def new_id(self):
        return str(self.last_id + 1)

    new_id = property(new_id)

    def get_products_for_test(self):
        self.clear()
        self.set_product(ProductDesc(item_id='1', desc='item1', price=100))
        self.set_product(ProductDesc(item_id='6', desc='item2', price=500))
        self.set_product(ProductDesc(item_id='2', desc='item23', price=600))
        self.set_product(ProductDesc(item_id='3', desc='item4', price=700))
        self.set_product(ProductDesc(item_id='4', desc='item5', price=300))
        return self
