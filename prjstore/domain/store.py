from contracts import contract

from prjstore.domain.item import Item
from prjstore.domain.product_catalog import ProductCatalog, get_products_for_test


class Store:
    """
>>> store = Store(test=True)
>>> store.items
[<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>]
>>> store.get_item_by_pr_id('4')
<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>
>>> store.search(name = 'item2')                                    # search items bu product nameription
[<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>\
]


    """

    def __init__(self, test=False):
        self._items = []
        self.is_test = test
        if test:
            self.pc = get_products_for_test()
            self.get_test_items()
        else:
            self.pc = ProductCatalog()
            self.get_items()

    def get_items(self):
        return self._items

    @contract(item=Item)
    def set_item(self, item):
        self._items.append(item)

    items = property(get_items, set_item)

    def get_items(self):
        pass

    @contract(pr_id=str)
    def get_item_by_pr_id(self, pr_id):
        for item in self._items:
            if item.product.id == pr_id:
                return item
        raise IndexError(f"Invalid product id: {pr_id}")

    @contract(name="None | str")
    def search(self, name=None) -> list:
        items = []
        if name:
            for item in self._items:
                if name in item.product.name:
                    items.append(item)
        return items

    def get_test_items(self):
        self.set_item(Item(pr=self.pc['2'], qty=3))
        self.set_item(Item(pr=self.pc['4'], qty=1))
        self.set_item(Item(pr=self.pc['6'], qty=2))
