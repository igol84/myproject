from prjstore.db.api.authorization import auth
from prjstore.db.api.components.seller import API_Seller


class API_DB:
    def __init__(self):
        self.headers = auth()
        self.seller = API_Seller(self.headers)


if __name__ == '__main__':
    db = API_DB()
    seller = db.seller.get(seller_id=2)
    print(seller)
    sellers = db.seller.get_all()
    print(sellers)
    print(len(sellers))
    print(list(sellers.values())[0])
