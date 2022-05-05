from typing import Optional

from prjstore.ui.pyside.interface_observer import ObserverInterface
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface


class AbstractModule(ObserverInterface):
    __parent: Optional[MainWindowInterface]
    __name: str
    __observer_module_names: list[str]
    __need_update: bool

    def __init__(self, parent=None):
        self.__parent = parent
        if parent:
            self.parent.register_observer(self)
            self.__name = ''
            self.__observer_module_names = []
            self.__need_update = True

    def __get_name(self) -> str:
        return self.__name

    def __set_name(self, name: str) -> None:
        self.__name = name

    name = property(__get_name, __set_name)

    def __get_parent(self) -> Optional[MainWindowInterface]:
        return self.__parent

    parent = property(__get_parent)

    def __get_need_update(self) -> bool:
        return self.__need_update

    def __set_need_update(self, flag: bool) -> None:
        self.__need_update = flag

    need_update = property(__get_need_update, __set_need_update)

    def __get_observer_module_names(self) -> list[str]:
        return self.__observer_module_names

    def __set_observer_module_names(self, observer_module_names: list[str]) -> None:
        self.__observer_module_names = observer_module_names

    observer_module_names = property(__get_observer_module_names, __set_observer_module_names)

    def update_data(self) -> None:
        ...
