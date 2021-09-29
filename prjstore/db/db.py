from abc import ABC, abstractmethod


class DB(ABC):

    @abstractmethod
    def create(self, **kwargs):
        pass

    @abstractmethod
    def update(self, **kwargs):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get(self, **kwargs):
        pass

    @abstractmethod
    def delete(self, **kwargs) -> bool:
        pass
