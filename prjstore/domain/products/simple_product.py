from prjstore.domain.abstract_product import AbstractProduct


class SimpleProduct(AbstractProduct):
    """
>>> pr = SimpleProduct(item_id='2', desc='item2', price=700)# Create product
>>> pr                                                    # Get product
<SimpleProduct: id=2, desc=item2, price=UAH 700.00>
>>> pr.id                                                 # Get id
'2'
>>> pr.desc = 'new item'                                  # Change desc
>>> print(pr.desc)                                        # Get desc
new item
>>> pr.price = 750.50                                     # Change price
>>> print(pr.price)                                       # Get price
UAH 750.50
>>> pr.convert_price('USD')                                    # Convert Price
>>> print(pr.price)
USD 27.29
>>> pr.edit(desc='item3', price=500, currency='USD')      # Edit product
>>> pr
<SimpleProduct: id=2, desc=item3, price=USD 500.00>
>>> pr.edit(desc='item2')                                 # Edit name
>>> pr
<SimpleProduct: id=2, desc=item2, price=USD 500.00>
>>> pr.edit(price=300)                                    # Edit desc
>>> pr
<SimpleProduct: id=2, desc=item2, price=USD 300.00>
    """

    def edit(self, desc=None, price=None, currency=None) -> None:
        AbstractProduct.edit(self, desc, price, currency)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}, desc={self.desc}, price={self.price}>'
