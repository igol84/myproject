from contracts import contract

from prjstore.domain.item import Item
from prjstore.domain.place_of_sale import PlaceOfSale
from prjstore.domain.product_catalog import ProductCatalog, get_products_for_test
from prjstore.domain.product_factory import ProductFactory
from prjstore.domain.seller import Seller


class Store:
    """
>>> store = Store(test=True)
>>> len(store.items)
4
>>> store.get_item_by_pr_id('4')
<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>
>>> store.search_item(name = 'item2')
{'2': <Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 '6': <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>}
>>> store.sellers
[<Seller: name=Igor>, <Seller: name=Anna>, <Seller: name=Sasha>]
>>> store.places_of_sale
[<PlaceOfSale: name: Интернет, sale:No>, <PlaceOfSale: name: Бокс 47, sale:No>, \
<PlaceOfSale: name: Магазин 1-й этаж, sale:No>, <PlaceOfSale: name: Магазин 2-й этаж, sale:No>]

    """

    def __init__(self, test=False):
        self.factory = ProductFactory()
        self.setup_product_catalog()
        self.setup_items()
        self.setup_sellers()
        self.setup_places_of_sale()

        if test:
            self.pc = get_products_for_test()
            self.items = get_test_items(self.pc)
            self.sellers = get_test_sellers()
            self.places_of_sale = get_test_places_of_sale()

    def setup_product_catalog(self):
        self.pc = ProductCatalog()

    def get_pc(self):
        return self._pc

    @contract(pc=ProductCatalog)
    def set_pc(self, pc):
        self._pc = pc

    pc = property(get_pc, set_pc)

    def setup_items(self):
        self._items = {}

    def setup_sellers(self):
        self._sellers = []

    def setup_places_of_sale(self):
        self._places_of_sale = []

    def get_items(self) -> dict[str: Item]:
        return self._items

    @contract(items='dict(str: $Item)')
    def set_items(self, items):
        self._items = items

    items = property(get_items, set_items)

    def get_sellers(self) -> list[Seller]:
        return self._sellers

    @contract(sellers='list($Seller)')
    def set_sellers(self, sellers):
        self._sellers = sellers

    sellers = property(get_sellers, set_sellers)

    def get_places_of_sale(self) -> list[PlaceOfSale]:
        return self._places_of_sale

    @contract(places_of_sale='list($PlaceOfSale)')
    def set_places_of_sale(self, places_of_sale):
        self._places_of_sale = places_of_sale

    places_of_sale = property(get_places_of_sale, set_places_of_sale)

    @contract(pr_id=str)
    def get_item_by_pr_id(self, pr_id):
        for it_id in self.items:
            if it_id == pr_id:
                return self.items[it_id]
        raise IndexError(f"Invalid product id: {pr_id}")

    @contract(name="None | str")
    def search_item(self, name=None) -> dict[str: Item]:
        items = {}
        if name:
            for it_id, item in self.items.items():
                if name in item.product.name:
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
