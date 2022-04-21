from prjstore.db.api import settings
from prjstore.db import schemas
from prjstore.db.api.authorizations import auth
from prjstore.db.api.components.seller import API_Seller
from prjstore.db.api.components.product import API_Product
from prjstore.db.api.components.product_catalog import API_ProductCatalog
from prjstore.db.api.components.item import API_Item
from prjstore.db.api.components.sale import API_Sale
from prjstore.db.api.components.sale_line_item import API_SaleLineItem
from prjstore.db.api.components.place import API_Place
from prjstore.db.api.components.expense import API_Expense
from prjstore.db.api.components.store import API_Store
from prjstore.db.api.components.handler_sale_registration import API_HandlerSaleRegistration
from prjstore.db.api.components.handler_receiving_the_items import API_HandlerReceivingTheItems
from prjstore.db.api.components.handler_product_price_editor import API_HandlerProductPriceEditor
from prjstore.db.api.components.handler_items_editor import API_HandlerItemEditor


class API_DB:
    def __init__(self, user_data=settings.user_data):
        self.headers = auth(user_data)
        self.seller = API_Seller(self.headers)
        self.product = API_Product(self.headers)
        self.product_catalog = API_ProductCatalog(self.headers)
        self.item = API_Item(self.headers)
        self.sale = API_Sale(self.headers)
        self.place = API_Place(self.headers)
        self.expense = API_Expense(self.headers)
        self.sale_line_item = API_SaleLineItem(self.headers)
        self.store = API_Store(self.headers)
        self.header_sale_registration = API_HandlerSaleRegistration(self.headers)
        self.header_receiving_the_items = API_HandlerReceivingTheItems(self.headers)
        self.handler_product_price_editor = API_HandlerProductPriceEditor(self.headers)
        self.handler_items_editor = API_HandlerItemEditor(self.headers)


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
