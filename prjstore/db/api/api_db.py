from prjstore.db import schemas
from prjstore.db.api.authorization import auth
from prjstore.db.api.components.seller import API_Seller
from prjstore.db.api.components.product import API_Product
from prjstore.db.api.components.product_catalog import API_ProductCatalog
from prjstore.db.api.components.item import API_Item
from prjstore.db.api.components.sale import API_Sale
from prjstore.db.api.components.sale_line_item import API_SaleLineItem
from prjstore.db.api.components.store import API_Store


class API_DB:
    def __init__(self):
        self.headers = auth()
        self.sore = API_Store(self.headers)
        self.seller = API_Seller(self.headers)
        self.product = API_Product(self.headers)
        self.product_catalog = API_ProductCatalog(self.headers)
        self.item = API_Item(self.headers)
        self.sale = API_Sale(self.headers)
        self.sale_line_item = API_SaleLineItem(self.headers)


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
