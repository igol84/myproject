from abc import ABC, abstractmethod

from prjstore.domain.abstract_product import AbstractProduct
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
    def create_seller(self, **kwargs) -> Seller:
        pass

    @abstractmethod
    def update_seller(self, pr_id: int, **kwargs) -> Seller:
        pass

    @abstractmethod
    def get_seller(self, pr_id: int) -> Seller:
        pass

    @abstractmethod
    def get_sellers(self) -> list[Seller]:
        pass

