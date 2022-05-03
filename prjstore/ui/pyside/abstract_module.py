from typing import Optional

from prjstore.ui.pyside.interface_observer import ObserverInterface
from prjstore.ui.pyside.main_window.main_interface import MainWindowInterface


class AbstractModule(ObserverInterface):
    __parent: Optional[MainWindowInterface]
    __need_update: bool

    def __init__(self, parent = None):
        self.__parent = parent
        if parent:
            self.parent.register_observer(self)
            self.__need_update: bool = True

    def __get_parent(self) -> Optional[MainWindowInterface]:
        return self.__parent

    parent = property(__get_parent)

    def __get_need_update(self) -> bool:
        return self.__need_update

    def __set_need_update(self, flag: bool) -> None:
        self.__need_update = flag

    need_update = property(__get_need_update, __set_need_update)

    def update_data(self) -> None:
        ...