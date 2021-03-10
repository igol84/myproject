from contracts import contract

from prjstore.domain.item import Item
from prjstore.domain.product_catalog import ProductCatalog, get_products_for_test


class Store:
    """
>>> store = Store(test=True)
>>> store.items
[<Item: product=<SimpleProduct: id=2, name=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<Shoes: id=3, name=item4, price=UAH 700.00, color=red, size=43.3,\
 length_of_insole=28.0, width=Medium>, qty=1>,\
 <Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<SimpleProduct: id=6, name=item2, price=UAH 500.00>, qty=2>]
>>> store.get_item_by_pr_id('4')
<Item: product=<SimpleProduct: id=4, name=item5, price=UAH 300.00>, qty=1>
>>> store.search_item(name = 'item2')                                    # search items by product name
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

    @contract(items=list)
    def set_items(self, items):
        for item in items:
            self.set_item(item)

    items = property(get_items, set_item)

    @contract(pr_id=str)
    def get_item_by_pr_id(self, pr_id):
        for item in self.items:
            if item.product.id == pr_id:
                return item
        raise IndexError(f"Invalid product id: {pr_id}")

    @contract(name="None | str")
    def search_item(self, name=None) -> list:
        items = []
        if name:
            for item in self.items:
                if name in item.product.name:
                    items.append(item)
        return items

    def get_test_items(self):
        items = [Item(pr=self.pc['2'], qty=3), Item(pr=self.pc['3'], qty=1),
                 Item(pr=self.pc['4'], qty=1), Item(pr=self.pc['6'], qty=2)]
        self.set_items(items)
