from prjstore.db.api.authorization import auth
from prjstore.db.api.components.seller import API_Seller
from prjstore.db.api.components.product import API_Product
from prjstore.db.api.components.item import API_Item
from prjstore.db.api.components.sale_line_item import API_SaleLineItem
from prjstore.db.api.components.store import API_Store


class API_DB:
    def __init__(self):
        self.headers = auth()
        self.sore = API_Store(self.headers)
        self.seller = API_Seller(self.headers)
        self.product = API_Product(self.headers)
        self.item = API_Item(self.headers)
        self.sale_line_item = API_SaleLineItem(self.headers)


if __name__ == '__main__':
    db = API_DB()
    store = db.sore.get(store_id=1)
    print(store.pc)
    # sellers = db.seller.get_all()
    # print(sellers)
    # print(len(sellers))
    # print(list(sellers.values())[0])
