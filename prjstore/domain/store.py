from contracts import contract

from item import Item
from product_catalog import ProductCatalog, get_products_for_test


class Store:
    """
>>> store = Store(test=True)
>>> store.items
[<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>,\
 <Item: product=<Product: id=6, desc=item2, price=UAH 500.00>, qty=2>]
>>> store.get_item_by_pr_id('4')
<Item: product=<Product: id=4, desc=item5, price=UAH 300.00>, qty=1>
>>> store.search(desc = 'item2')                                    # search items bu product description
[<Item: product=<Product: id=2, desc=item23, price=UAH 600.00>, qty=3>,\
 <Item: product=<Product: id=6, desc=item2, price=UAH 500.00>, qty=2>]


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

    @contract
    def set_item(self, item: "isinstance(Item)"):
        self._items.append(item)

    items = property(get_items, set_item)

    def get_items(self):
        pass

    @contract
    def get_item_by_pr_id(self, pr_id: "str"):
        for item in self._items:
            if item.product.id == pr_id:
                return item
        else:
            raise IndexError(f"Invalid product id: {pr_id}")

    def search(self, desc=None) -> list:
        items = []
        if desc:
            for item in self._items:
                if desc in item.product.desc:
                    items.append(item)
        return items

    def get_test_items(self):
        self.set_item(Item(pr=self.pc['2'], qty=3))
        self.set_item(Item(pr=self.pc['4'], qty=1))
        self.set_item(Item(pr=self.pc['6'], qty=2))
