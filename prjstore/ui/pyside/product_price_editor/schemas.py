from typing import Optional

from pydantic import BaseModel

from prjstore.domain.item import Item
from prjstore.domain.products.shoes import Shoes


class ModelShoes(BaseModel):
    size: float
    color: Optional[str] = None
    length: Optional[float] = None
    width: Optional[str] = None
    width_of_insole: Optional[float] = None


class ModelProduct(BaseModel):
    prod_id: str
    name: str
    price: float
    price_format: str
    qty: int
    type: str = ''
    shoes: Optional[ModelShoes] = None

    def get_desc(self) -> str:
        if self.shoes:
            desc = self.name
            desc += f' {self.shoes.color}' if self.shoes.color else ''
            desc += f' {self.shoes.width}' if self.shoes.width else ''
            desc += f' {self.shoes.size:g}'
        else:
            desc = self.name
        return desc


class ProductId(str):
    pass


class Price(float):
    pass


class ViewProduct(ModelProduct):
    pass


class ViewSize(BaseModel):
    prod_id: str
    size: float
    length_of_insole: float | None
    price: float
    price_format: str
    qty: int


class ViewWidth(BaseModel):
    width: Optional[str] = None
    sizes: list[ViewSize]


class ViewColor(BaseModel):
    color: Optional[str] = None
    widths: list[ViewWidth]


class ViewShoes(BaseModel):
    type: str = 'shoes'
    name: str
    colors: list[ViewColor]


def create_product_schemas_by_items(items: dict[int: Item]) -> list[ViewProduct]:
    # creating data
    products: dict[str: ModelProduct] = {}
    for item_ in items.values():
        if item_.qty > 0:
            if item_.product.prod_id not in products:
                shoes = None
                if item_.product.product_type == 'shoes' and isinstance(item_.product, Shoes):
                    size = item_.product.size
                    color = item_.product.color
                    width = getattr(item_.product.width, 'short_name', None)
                    length = item_.product.length_of_insole
                    insole = getattr(item_.product.width, 'width_of_insole', 0)
                    shoes = ModelShoes(size=size, color=color, length=length, width=width, width_of_insole=insole)
                products[item_.product.prod_id] = ModelProduct(
                    prod_id=item_.product.prod_id,
                    type=item_.product.product_type,
                    name=item_.product.name,
                    price=item_.product.price.amount,
                    price_format=item_.product.price.format(),
                    qty=item_.qty,
                    shoes=shoes
                )
            else:
                products[item_.product.prod_id].qty += item_.qty
    # sorting data
    sorted_products = sorted(products.values(), key=lambda k: (
        k.name, getattr(k.shoes, 'color', None), getattr(k.shoes, 'width_of_insole', 0),
        getattr(k.shoes, 'size', 0)))

    # grouping data
    products = []
    for product in sorted_products:
        if product.type == 'shoes':
            last_item_type = products[-1].type if products else None
            size = ViewSize(prod_id=product.prod_id, size=product.shoes.size, length_of_insole=product.shoes.length,
                            price=product.price, price_format=product.price_format, qty=product.qty)
            width = ViewWidth(width=product.shoes.width, sizes=[size])
            color = ViewColor(color=product.shoes.color, widths=[width])
            if last_item_type != 'shoes' or (last_item_type == 'shoes' and products[-1].name != product.name):
                shoes = ViewShoes(type=product.type, name=product.name, colors=[color])
                products.append(shoes)
            elif last_item_type == 'shoes' and products[-1].name == product.name:
                if products[-1].colors[-1].color != product.shoes.color:
                    products[-1].colors.append(color)
                else:
                    if products[-1].colors[-1].widths[-1].width != product.shoes.width:
                        products[-1].colors[-1].widths.append(width)
                    else:
                        products[-1].colors[-1].widths[-1].sizes.append(size)
        else:
            product = ViewProduct(prod_id=product.prod_id, type=product.type, name=product.name,
                                  price=product.price, price_format=product.price_format, qty=product.qty)
            products.append(product)
    return products
