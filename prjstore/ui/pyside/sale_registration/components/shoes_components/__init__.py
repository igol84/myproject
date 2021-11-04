from prjstore.ui.pyside.sale_registration.components.shoes_components.size import SizeFrame
from prjstore.ui.pyside.sale_registration.components.shoes_components.width import WidthFrame
from prjstore.ui.pyside.sale_registration.components.shoes_components.color import ColorFrame


class ShoesFrameInterface:
    def hide_colors(self) -> None:
        ...

    def show_colors(self) -> None:
        ...
