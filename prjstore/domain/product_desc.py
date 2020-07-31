"""
    >>> pr = ProductDesc(item_id=2, desc='item2', price=700)  # Create product
    >>> print(pr)                                             # print product object
    <Product: id=2, desc=item2, price=700>
    >>> pr.id                                                 # Get id
    2
    >>> pr.desc = 'newitem'                                   # Change desc
    >>> pr.desc                                               # Get desc
    'newitem'
    >>> pr.price = 750                                        # Change price
    >>> pr.price                                              # Get price
    750
    >>> pr.edit(desc='item3', price=500)                      # Edit product
    >>> print(pr)
    <Product: id=2, desc=item3, price=500>

    >>> pr2 = ProductDesc(desc='item3', price=800)            # Create new product with new generated id
    >>> print(pr2)
    <Product: id=3, desc=item3, price=800>


"""
from contracts import contract


class ProductDesc:
    __lid = 1  # counter of id product

    @contract
    def __init__(self, item_id=None, desc: 'str' = 'item', price=None):
        self._item_id = item_id if item_id else ProductDesc.__lid
        self._desc = desc
        self._price = float(price)
        ProductDesc.__lid = self._item_id + 1

    def __repr__(self):
        return f'<Product: id={self._item_id}, desc={self._desc}, price={self._price}>'

    def get_id(self):
        return self._item_id

    id = property(get_id)

    def get_price(self):
        return self._price

    def set_price(self, price):
        self._price = float(price)

    price = property(get_price, set_price)

    def get_desc(self):
        return self._desc

    @contract
    def set_desc(self, desc: 'str'):
        self._desc = desc

    desc = property(get_desc, set_desc)

    def edit(self, desc=None, price = None):
        if desc: self.set_desc(desc)
        if price: self.set_price(price)

