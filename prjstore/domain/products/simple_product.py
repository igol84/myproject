from pydantic.dataclasses import dataclass

from prjstore.domain.abstract_product import AbstractProduct
from util.money import Money, currencies


@dataclass
class SimpleProduct(AbstractProduct):
    """
>>> pr = SimpleProduct(prod_id='2', name='item2', price=Money(amount=700))# Create product
>>> pr                                                    # Get product
SimpleProduct(prod_id='2', name='item2', price=Money(amount=700.0, currency=Currency(code='UAH', rate=27.5, sign='₴')))
>>> pr.prod_id                                                 # Get id
'2'
>>> pr.name = 'new item'                                  # Change name
>>> print(pr.name)                                        # Get name
new item
>>> pr.price = Money(amount=750.50)                                    # Change price
>>> print(pr.price.amount)                                       # Get price
750.5
>>> pr.convert_price('USD')                                    # Convert Price
>>> print(pr.price.amount)
27.29
>>> pr.edit(name='item3', price='500', currency='USD')      # Edit product
>>> print(pr.name, pr.price.format())
item3 500.00$
    """
