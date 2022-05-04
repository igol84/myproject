from prjstore.db import API_DB
from prjstore.db.schemas import seller as db_schemas
from prjstore.domain.seller import Seller
from prjstore.domain.store import Store
from prjstore.handlers.abstract_module_handler import AbstractModuleHandler
from prjstore.handlers.main_handler import MainHandler
from prjstore.ui.pyside.sellers_editor import schemas


class SellersEditorHandler(AbstractModuleHandler):
    db: API_DB
    store: Store

    def __init__(self, db: API_DB = None, main_handler: MainHandler = None):
        super().__init__(db, main_handler)

    def get_store_sellers(self) -> list[schemas.ViewSeller]:
        sellers: dict[int: Seller] = self.store.sellers
        list_pd_sellers = []
        for seller_id, seller in sellers.items():
            pd_seller = schemas.ViewSeller(seller_id=seller_id, name=seller.name, active=seller.active)
            list_pd_sellers.append(pd_seller)
            list_pd_sellers.sort(key=lambda k: k.seller_id, reverse=True)
        return list_pd_sellers

    def edit_name(self, seller_id: int, new_name: str):
        # edit on DB
        pd_seller: db_schemas.UpdateSeller = self.db.seller.edit_name(seller_id, new_name)
        # edit in Domain Model
        self.store.sellers[pd_seller.id].name = pd_seller.name
        return pd_seller

    def edit_active(self, seller_id: int, active: bool):
        # edit on DB
        pd_seller: db_schemas.UpdateSeller = self.db.seller.edit_active(seller_id, active)
        # edit in Domain Model
        self.store.sellers[pd_seller.id].active = pd_seller.active
        return pd_seller

    def add_seller(self, name: str):
        # edit on DB
        store_id = self.store.id
        pd_create_seller = db_schemas.CreateSeller(store_id=store_id, name=name, active=True)
        pd_seller: db_schemas.Seller = self.db.seller.create(pd_create_seller)
        # edit in Domain Model

        self.store.sellers[pd_seller.id] = Seller(id=pd_seller.id, name=pd_seller.name, active=pd_seller.active)
        return pd_seller
