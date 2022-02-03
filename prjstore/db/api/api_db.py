from prjstore.db import schemas
from prjstore.db.api.authorization import auth
from prjstore.db.api.components.seller import API_Seller
from prjstore.db.api.components.product import API_Product
from prjstore.db.api.components.product_catalog import API_ProductCatalog
from prjstore.db.api.components.item import API_Item
from prjstore.db.api.components.sale import API_Sale
from prjstore.db.api.components.sale_line_item import API_SaleLineItem
from prjstore.db.api.components.place import API_Place
from prjstore.db.api.components.store import API_Store
from prjstore.db.api.components.header_sale_registration import API_HeaderSaleRegistration
from prjstore.db.api.components.header_receiving_the_items import API_HeaderReceivingTheItems


class API_DB:
    def __init__(self):
        self.headers = auth()
        self.seller = API_Seller(self.headers)
        self.product = API_Product(self.headers)
        self.product_catalog = API_ProductCatalog(self.headers)
        self.item = API_Item(self.headers)
        self.sale = API_Sale(self.headers)
        self.place = API_Place(self.headers)
        self.sale_line_item = API_SaleLineItem(self.headers)
        self.store = API_Store(self.headers)
        self.header_sale_registration = API_HeaderSaleRegistration(self.headers)
        self.header_receiving_the_items = API_HeaderReceivingTheItems(self.headers)


if __name__ == '__main__':
    from datetime import datetime
    from prjstore.db.schemas.sale_line_item import CreateSaleLineItemForSale

    db = API_DB()
    sale_line_items = [CreateSaleLineItemForSale(item_id=1, sale_price=2, qty=1),
                       CreateSaleLineItemForSale(item_id=2, sale_price=20, qty=1)]
    pd_sale = schemas.sale.CreateSale(place_id=1, seller_id=1, date_time=datetime.now(),
                                      sale_line_items=sale_line_items)
    db.sale.create(pd_sale)

    # sellers = db.seller.get_all()
    # print(sellers)
    # print(len(sellers))
    # print(list(sellers.values())[0])
