from abc import ABC, abstractmethod

from prjstore.domain.seller import Seller


class DB(ABC):

    # @abstractmethod
    # def create_product(self, **kwargs) -> AbstractProduct:
    #     pass
    #
    # @abstractmethod
    # def update_product(self, pr_id: int, **kwargs) -> AbstractProduct:
    #     pass
    #
    # @abstractmethod
    # def get_product(self, pr_id: int) -> AbstractProduct:
    #     pass
    #
    # @abstractmethod
    # def get_products(self) -> list[AbstractProduct]:
    #     pass

    @abstractmethod
    def create_seller(self, **kwargs) -> dict[int: Seller]:
        pass

    @abstractmethod
    def update_seller(self, seller_id: int, store_id:int, name:str) -> dict[int: Seller]:
        pass

    @abstractmethod
    def get_all_sellers(self) -> dict[int: Seller]:
        pass

    @abstractmethod
    def get_seller(self, seller_id: int) -> dict[int: Seller]:
        pass

    @abstractmethod
    def delete_seller(self, seller_id: int) -> bool:
        pass
