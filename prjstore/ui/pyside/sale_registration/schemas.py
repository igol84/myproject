from collections import OrderedDict
from typing import Optional

from pydantic import BaseModel

from prjstore.db.schemas.sale import ShowSaleWithSLIs
from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.products.shoes import Shoes
from prjstore.domain.sale import Sale
from prjstore.domain.sale_line_item import SaleLineItem


class ModelShoes(BaseModel):
    size: float
    color: Optional[str] = None
    length: Optional[float] = None
    width: Optional[str] = None
    width_of_insole: Optional[float] = None


class ModelSale(BaseModel):
    sale: Sale
    place: PlaceOfSale


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


class ViewSeller(BaseModel):
    id: int
    desc: str


class ViewPlace(BaseModel):
    id: int
    desc: str


class ViewSale(BaseModel):
    id: int
    place: ViewPlace
    seller: ViewSeller
    products: list[ViewProduct]


class ViewSize(BaseModel):
    prod_id: str
    size: float
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
            size = ViewSize(prod_id=product.prod_id, size=product.shoes.size, price=product.price,
                            price_format=product.price_format, qty=product.qty)
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


def create_sli_schemas_by_items(list_sli: list[SaleLineItem]) -> dict[tuple[ProductId, Price], ModelProduct]:
    products: dict[tuple[ProductId, Price], ModelProduct] = {}
    for sli in list_sli:
        shoes = None
        if sli.item.product.product_type == 'shoes' and isinstance(sli.item.product, Shoes):
            width = getattr(sli.item.product.width, 'short_name', None)
            width_of_insole = getattr(sli.item.product.width, 'width_of_insole', None)
            shoes = ModelShoes(size=sli.item.product.size, color=sli.item.product.color,
                               length=sli.item.product.length_of_insole, width=width, width_of_insole=width_of_insole)
        if (sli.item.product.prod_id, sli.sale_price.amount) not in products:
            products[sli.item.product.prod_id, sli.sale_price.amount] = ModelProduct(
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


def create_sale_schemas_by_ledger(ledger: dict[int, ModelSale]) -> list[ViewSale]:
    list_sales = []
    for model in ledger.values():
        pd_place = model.place
        pd_sale = model.sale
        pd_place = ViewPlace(id=pd_place.id, desc=pd_place.name)
        pd_seller = ViewSeller(id=pd_sale.seller.id, desc=pd_sale.seller.name)
        products: dict[tuple[ProductId, Price], ModelProduct] = create_sli_schemas_by_items(pd_sale.list_sli)
        products_list = [product for product in products.values()]
        pd_sale = ViewSale(id=pd_sale.id, place=pd_place, seller=pd_seller, products=products_list)
        list_sales.append(pd_sale)
    return sorted(list_sales, key=lambda sale: (sale.place.id, sale.seller.id))


class ModelsSeller(BaseModel):
    seller_id: int
    desc: str

    def __hash__(self):
        return hash(self.seller_id)


class ModelsPlace(BaseModel):
    place_id: int
    desc: str

    def __hash__(self):
        return hash(self.place_id)


class SaleId(int):
    pass


class PlaceId(int):
    pass


class SellerId(int):
    pass


def create_sales_by_sales_schemas(pd_sales: list[ShowSaleWithSLIs]) -> dict[int, tuple[Sale, PlaceOfSale]]:
    sales_by_date: dict[int, Sale] = {}
    for pd_sale in pd_sales:
        sale = Sale.create_from_schema(pd_sale)
        place = PlaceOfSale.create_from_schema(pd_sale.place)
        sales_by_date[sale.id] = ModelSale(sale=sale, place=place)
    return OrderedDict(sorted(sales_by_date.items()))
