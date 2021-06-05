from decimal import Decimal
from typing import Optional, Union

from prjstore.domain.abstract_product import AbstractProduct
from util.money_my import Money


class SimpleProduct(AbstractProduct):
    """
>>> pr = SimpleProduct(product_id='2', name='item2', price=700)# Create product
>>> pr                                                    # Get product
<SimpleProduct: id=2, name=item2, price=UAH 700.00>
>>> pr.id                                                 # Get id
'2'
>>> pr.name = 'new item'                                  # Change name
>>> print(pr.name)                                        # Get name
new item
>>> pr.price = 750.50                                     # Change price
>>> print(pr.price)                                       # Get price
UAH 750.50
>>> pr.convert_price('USD')                                    # Convert Price
>>> print(pr.price)
USD 27.29
>>> pr.edit(name='item3', price=500, currency='USD')      # Edit product
>>> pr
<SimpleProduct: id=2, name=item3, price=USD 500.00>
>>> pr.edit(name='item2')                                 # Edit name
>>> pr
<SimpleProduct: id=2, name=item2, price=USD 500.00>
>>> pr.edit(price=300)                                    # Edit name
>>> pr
<SimpleProduct: id=2, name=item2, price=USD 300.00>
    """

    def edit(self,
             name: Optional[str] = None,
             price: Union[None, Money, int, float, Decimal] = None,
             currency: Optional[str] = None
             ) -> None:
        AbstractProduct.edit(self, name, price, currency)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: id={self.id}, name={self.name}, price={self.price}>'
