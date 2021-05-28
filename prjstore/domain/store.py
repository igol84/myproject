from contracts import contract

from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.product_catalog import ProductCatalog, get_products_for_test
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.seller import Seller


class Store:
    """
>>> store = Store()
>>> store.pc = get_products_for_test()
>>> store.items = get_test_items(store.pc)
>>> store.sellers = get_test_sellers()
>>> store.places_of_sale = get_test_places_of_sale()
>>> len(store.items)
4
>>> store.get_item_by_pr_id('4')
<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>
>>> store.search_items_by_name(name = 'item2')
{'2': <Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 '6': <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>}
>>> store.sellers
[<Seller: name=Igor>, <Seller: name=Anna>, <Seller: name=Sasha>]
>>> store.places_of_sale
[<PlaceOfSale: name: Интернет, sale:No>, <PlaceOfSale: name: Бокс 47, sale:No>, \
<PlaceOfSale: name: Магазин 1-й этаж, sale:No>, <PlaceOfSale: name: Магазин 2-й этаж, sale:No>]
>>> store.items
{'2': <Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>, '3': <Item: product=\
<Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0, width=Medium>, qty=1>, '4': \
<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, '6': <Item: product=\
<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>}
>>> item = store.items['2']
>>> del store.items['2']
>>> item.qty = 0
>>> store.items
{'3': <Item: product=<Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3, length_of_insole=28.0, \
width=Medium>, qty=1>, '4': <Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>, '6': \
<Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>}
>>> store.add_item(item, 3)
>>> store.items['2']
<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>
>>> store.add_item(item)
>>> store.items['2']
<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=4>


    """

    def __init__(self):
        self.factory: ProductFactory = ProductFactory()
        self.pc: ProductCatalog = ProductCatalog()
        self.__items: dict[str, Item] = {}
        self.__sellers: list[Seller] = []
        self.__places_of_sale: list[PlaceOfSale] = []

    ###############################################################################################
    # pc
    def __get_pc(self) -> ProductCatalog:
        return self.__pc

    @contract(pc=ProductCatalog)
    def __set_pc(self, pc: ProductCatalog) -> None:
        self.__pc = pc

    pc = property(__get_pc, __set_pc)

    ###############################################################################################
    # items
    def __get_items(self) -> dict[str: Item]:
        return self.__items

    @contract(items='dict(str: $Item)')
    def __set_items(self, items: dict[str, Item]) -> None:
        self.__items = items

    items = property(__get_items, __set_items)

    ###############################################################################################
    # sellers
    def __get_sellers(self) -> list[Seller]:
        return self.__sellers

    @contract(sellers='list($Seller)')
    def __set_sellers(self, sellers: list[Seller]):
        self.__sellers = sellers

    sellers = property(__get_sellers, __set_sellers)

    ###############################################################################################
    # places_of_sale
    def __get_places_of_sale(self) -> list[PlaceOfSale]:
        return self.__places_of_sale

    @contract(places_of_sale='list($PlaceOfSale)')
    def __set_places_of_sale(self, places_of_sale: list[PlaceOfSale]) -> None:
        self.__places_of_sale = places_of_sale

    places_of_sale = property(__get_places_of_sale, __set_places_of_sale)

    ###############################################################################################
    @contract(pr_id=str)
    def get_item_by_pr_id(self, pr_id: str) -> Item:
        if pr_id in self.items:
            return self.items[pr_id]
        raise IndexError(f"Invalid product id: {pr_id}")

    @contract(name="None | str")
    def search_items_by_name(self, name: str = None) -> dict[str: Item]:
        items = {}
        if name:
            for it_id, item in self.items.items():
                if name.lower() in item.product.name.lower():
                    items[it_id] = item
        return items

    @contract(item=Item, qty=int)
    def add_item(self, item: Item, qty: int = 1):
        if item.product.id not in self.items:
            self.items[item.product.id] = item
        self.items[item.product.id].qty += qty


###############################################################################################
# For Test
def get_test_items(pc: ProductCatalog) -> dict[str, Item]:
    items = {'2': Item(pc['2'], qty=3), '3': Item(pc['3'], qty=1),
             '4': Item(pc['4'], qty=1), '6': Item(pc['6'], qty=2)}
    return items


def get_test_sellers() -> list[Seller]:
    sellers = [Seller('Igor'), Seller('Anna'), Seller('Sasha')]
    return sellers


def get_test_places_of_sale() -> list[PlaceOfSale]:
    places_of_sale = [PlaceOfSale('Интернет'), PlaceOfSale('Бокс 47'),
                      PlaceOfSale('Магазин 1-й этаж'), PlaceOfSale('Магазин 2-й этаж')]
    return places_of_sale
