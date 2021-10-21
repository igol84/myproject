from typing import Optional

from pydantic import BaseModel

from prjstore.domain.item import Item
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.sale_line_item import SaleLineItem


class ViewShoes(BaseModel):
    size: float
    color: Optional[str] = None
    length: Optional[float] = None
    width: Optional[str] = None


class ViewProduct(BaseModel):
    prod_id: int
    name: str
    price: float
    price_format: str
    qty: int
    type: Optional[str] = None
    shoes: Optional[ViewShoes] = None


def create_product_schemas_by_items(items: dict[int: Item]) -> dict[str: ViewProduct]:
    products: dict[str: ViewProduct] = {}
    for item_ in items.values():
        if item_.product.prod_id not in products:
            shoes = None
            if item_.product.product_type == 'shoes' and isinstance(item_.product, Shoes):
                width = item_.product.width.short_name if item_.product.width else None
                shoes = ViewShoes(size=item_.product.size, color=item_.product.color,
                                  length=item_.product.length_of_insole, width=width)
            products[item_.product.prod_id] = ViewProduct(
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
    return products


def create_sli_schemas_by_items(list_sli: list[SaleLineItem]) -> dict[str: ViewProduct]:
    products: dict[tuple[str, float]: ViewProduct] = {}
    for sli in list_sli:
        shoes = None
        if sli.item.product.product_type == 'shoes' and isinstance(sli.item.product, Shoes):
            width = sli.item.product.width.short_name if sli.item.product.width else None
            shoes = ViewShoes(size=sli.item.product.size, color=sli.item.product.color,
                              length=sli.item.product.length_of_insole, width=width)
        if (sli.item.product.prod_id, sli.sale_price.amount) not in products:
            products[sli.item.product.prod_id, sli.sale_price.amount] = ViewProduct(
                prod_id=sli.item.product.prod_id,
                type=sli.item.product.product_type,
                name=sli.item.product.name,
                price=sli.sale_price.amount,
                price_format=sli.sale_price.format(),
                qty=sli.qty,
                shoes=shoes

            )
        else:
            products[sli.item.product.prod_id, sli.sale_price.amount].qty += sli.qty
    return products
