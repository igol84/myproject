from contracts import contract

from .item import Item
from .place_of_sale import PlaceOfSale
from .product_catalog import ProductCatalog, get_products_for_test
from .product_factory import ProductFactory
from .seller import Seller


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

    """

    def __init__(self):
        self.factory = ProductFactory()
        self.setup_product_catalog()
        self.setup_items()
        self.setup_sellers()
        self.setup_places_of_sale()

    def setup_product_catalog(self):
        self.pc = ProductCatalog()

    def get_pc(self):
        return self.__pc

    @contract(pc=ProductCatalog)
    def set_pc(self, pc):
        self.__pc = pc

    pc = property(get_pc, set_pc)

    def setup_items(self):
        self.__items = {}

    def setup_sellers(self):
        self.__sellers = []

    def setup_places_of_sale(self):
        self.__places_of_sale = []

    def get_items(self) -> dict[str: Item]:
        return self.__items

    @contract(items='dict(str: $Item)')
    def set_items(self, items):
        self.__items = items

    items = property(get_items, set_items)

    def get_sellers(self) -> list[Seller]:
        return self.__sellers

    @contract(sellers='list($Seller)')
    def set_sellers(self, sellers):
        self.__sellers = sellers

    sellers = property(get_sellers, set_sellers)

    def get_places_of_sale(self) -> list[PlaceOfSale]:
        return self.__places_of_sale

    @contract(places_of_sale='list($PlaceOfSale)')
    def set_places_of_sale(self, places_of_sale):
        self.__places_of_sale = places_of_sale

    places_of_sale = property(get_places_of_sale, set_places_of_sale)

    @contract(pr_id=str)
    def get_item_by_pr_id(self, pr_id):
        for it_id in self.items:
            if it_id == pr_id:
                return self.items[it_id]
        raise IndexError(f"Invalid product id: {pr_id}")

    @contract(name="None | str")
    def search_items_by_name(self, name=None) -> dict[str: Item]:
        items = {}
        if name:
            for it_id, item in self.items.items():
                if name.lower() in item.product.name.lower():
                    items[it_id] = item
        return items


def get_test_items(pc):
    items = {'2': Item(pc['2'], qty=3), '3': Item(pc['3'], qty=1),
              '4': Item(pc['4'], qty=1), '6': Item(pc['6'], qty=2)}
    return items

def get_test_sellers():
    sellers = [Seller('Igor'), Seller('Anna'), Seller('Sasha')]
    return sellers

def get_test_places_of_sale():
    places_of_sale = [PlaceOfSale('Интернет'), PlaceOfSale('Бокс 47'),
                      PlaceOfSale('Магазин 1-й этаж'), PlaceOfSale('Магазин 2-й этаж')]
    return places_of_sale
