from contracts import contract

from product_desc import ProductDesc


class ProductCatalog(list):
    """
>>> pc = get_products_for_test()  # create get test products
>>> pc                         #
[<Product: id=1, desc=item1, price=UAH 100.00>,\
 <Product: id=2, desc=item23, price=UAH 600.00>,\
 <Product: id=3, desc=item4, price=UAH 700.00>,\
 <Product: id=4, desc=item5, price=UAH 300.00>,\
 <Product: id=6, desc=item2, price=UAH 500.00>]
>>> pc.quantity                                           # count of products
5
>>> pc.last_id                                           # get last id
6
>>> pc.new_id                                            # get new generated id  "last id + 1"
'7'
>>> pc.set_product(ProductDesc(item_id=pc.new_id))
>>> pc.set_product(ProductDesc(item_id=pc.new_id, desc='item12', price=300))
>>> pc                                                   # get catalog
[<Product: id=1, desc=item1, price=UAH 100.00>,\
 <Product: id=2, desc=item23, price=UAH 600.00>,\
 <Product: id=3, desc=item4, price=UAH 700.00>,\
 <Product: id=4, desc=item5, price=UAH 300.00>,\
 <Product: id=6, desc=item2, price=UAH 500.00>, \
<Product: id=7, desc=item, price=UAH 0.00>, \
<Product: id=8, desc=item12, price=UAH 300.00>]
>>> pc['2']                                              # get product by id='2'
<Product: id=2, desc=item23, price=UAH 600.00>
>>> f_products = []
>>> for pr in pc:                               # get products, where price > 500 UAH
...     if pr.price.UAH.amount > 500 :
...         f_products.append((pr.desc, pr.price.USD))
>>> f_products
[('item23', USD 21.82), ('item4', USD 25.45)]
>>> pc.set_product(ProductDesc(item_id=pc.new_id, desc='prod', price=500))
>>> pc                                                   # get catalog
[<Product: id=1, desc=item1, price=UAH 100.00>,\
 <Product: id=2, desc=item23, price=UAH 600.00>,\
 <Product: id=3, desc=item4, price=UAH 700.00>,\
 <Product: id=4, desc=item5, price=UAH 300.00>,\
 <Product: id=6, desc=item2, price=UAH 500.00>,\
 <Product: id=7, desc=item, price=UAH 0.00>,\
 <Product: id=8, desc=item12, price=UAH 300.00>, \
<Product: id=9, desc=prod, price=UAH 500.00>]
>>> pc.unset_product_by_pr_id('3')
>>> pc                                                   # get catalog
[<Product: id=1, desc=item1, price=UAH 100.00>,\
 <Product: id=2, desc=item23, price=UAH 600.00>,\
 <Product: id=4, desc=item5, price=UAH 300.00>,\
 <Product: id=6, desc=item2, price=UAH 500.00>,\
 <Product: id=7, desc=item, price=UAH 0.00>,\
 <Product: id=8, desc=item12, price=UAH 300.00>, \
<Product: id=9, desc=prod, price=UAH 500.00>]
>>> pc.search(desc='item2')                               # search products by name containing "item"
[<Product: id=2, desc=item23, price=UAH 600.00>,\
 <Product: id=6, desc=item2, price=UAH 500.00>]


    """

    def __init__(self):
        super().__init__()

    @contract
    def set_product(self, pr: "isinstance(ProductDesc)") -> None:
        self.append(pr)

    @contract
    def unset_product_by_pr_id(self, pr_id: "str") -> None:
        self.remove(self[pr_id])

    @contract
    def __setitem__(self, key: "str", value: "isinstance(ProductDesc)"):
        self.set_product(value)

    def __getitem__(self, key):
        return self.get_product_by_id(key)

    def get_product_by_id(self, key):
        for pr in self:
            if pr.id == key:
                return pr
        raise IndexError(f"Invalid product id: {key}")

    def search(self, desc=None) -> list:
        products = []
        if desc:
            for product in self:
                if desc in product.desc:
                    products.append(product)
        return products

    def quantity(self) -> int:
        return len(self)

    quantity = property(quantity)

    def last_id(self) -> int:
        return sorted([int(pr.id) for pr in self])[-1]

    last_id = property(last_id)

    def new_id(self) -> str:
        return str(self.last_id + 1)

    new_id = property(new_id)


def get_products_for_test():
    pc = ProductCatalog()
    pc.set_product(ProductDesc(item_id='1', desc='item1', price=100))
    pc.set_product(ProductDesc(item_id='2', desc='item23', price=600))
    pc.set_product(ProductDesc(item_id='3', desc='item4', price=700))
    pc.set_product(ProductDesc(item_id='4', desc='item5', price=300))
    pc.set_product(ProductDesc(item_id='6', desc='item2', price=500))
    return pc
