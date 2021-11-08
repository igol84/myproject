from PySide2 import QtWidgets
from PySide2.QtWidgets import QWidget, QApplication

from prjstore.ui.pyside.sale_registration.components.abstract_product import ItemFrame, Item
from prjstore.ui.pyside.sale_registration.components.shoes_components import ColorFrame, SizeFrame, ShoesDesc
from prjstore.ui.pyside.sale_registration.components.shoes_components.shoes_frame_interface import ShoesFrameInterface
from prjstore.ui.pyside.sale_registration.schemas import ViewShoes, ViewSize, ViewWidth, ViewColor
from prjstore.ui.pyside.utils.widgets import QHLine


class ShoesFrame(ItemFrame, Item, ShoesFrameInterface):
    # height_ = 130
    pr_name: str
    pr_price: float
    pr_colors: list[ViewColor]
    __selected_size_frame: SizeFrame = None

    def __init__(self, parent, item_pd: ViewShoes):
        super().__init__()
        self.__parent_form = parent
        self.pr_name = item_pd.name
        self.pr_price = 2.0
        self.pr_price_format = ''
        self.pr_colors = item_pd.colors

        layer = QtWidgets.QVBoxLayout()
        layer.setMargin(0)
        self.layer_desc = QtWidgets.QVBoxLayout()
        self.layer_desc.setMargin(0)
        self.label_item_description = ShoesDesc(parent=parent, pr_name=self.pr_name)
        self.layer_desc.addWidget(self.label_item_description)
        layer.addLayout(self.layer_desc)
        self.layer_colors = QtWidgets.QVBoxLayout()

        for n, view_color in enumerate(self.pr_colors):
            if n:
                line = QHLine()
                self.layer_colors.addWidget(line)
            self.color_frame = ColorFrame(shoes_frame=self, pd_color=view_color)
            self.layer_colors.addWidget(self.color_frame)
        layer.addLayout(self.layer_colors)
        self.setLayout(layer)
        self.hide_colors()

    def hide_colors(self):
        for n in range(self.layer_colors.count()):
            self.layer_colors.itemAt(n).widget().hide()

    def show_colors(self):
        for n in range(self.layer_colors.count()):
            self.layer_colors.itemAt(n).widget().show()

    def __get_parent_form(self):
        return self.__parent_form

    parent_form = property(__get_parent_form)

    def get_selected_size_frame(self) -> SizeFrame:
        return self.__selected_size_frame

    def set_selected_size_frame(self, size_frame: SizeFrame) -> None:
        if self.__selected_size_frame:
            self.__selected_size_frame.setStyleSheet(
                f"background-color: {self.default_color_bg}; color: {self.default_color_text}")
        self.__selected_size_frame = size_frame
        self.__selected_size_frame.setStyleSheet(
            f"background-color: {self.current_color_bg}; color: {self.current_color_text}")
        price_text = self.__selected_size_frame.pr_price
        self.label_item_description.price_line_edit.setText(f'{price_text:g}')
        self.label_item_description.price_line_edit.show()
        self.label_item_description.price_line_edit.setFocus()
        self.label_item_description.price_line_edit.selectAll()

    def del_selected_size_frame(self) -> None:
        self.__selected_size_frame = None

    selected_size_frame = property(get_selected_size_frame, set_selected_size_frame, del_selected_size_frame)


if __name__ == "__main__":
    import sys
    from PySide2.QtWidgets import QVBoxLayout

    app = QApplication(sys.argv)

    red_E_sizes = [
        ViewSize(prod_id='2', size=43, price=4000, price_format='4.000грн', qty=5),
        ViewSize(prod_id='3', size=44, price=4000, price_format='4.000грн', qty=2),
        ViewSize(prod_id='4', size=45, price=2000, price_format='2.000грн', qty=1),
    ]
    red_D_sizes = [
        ViewSize(prod_id='5', size=41, price=4000, price_format='3.000грн', qty=1),
        ViewSize(prod_id='6', size=42, price=4000, price_format='2.000грн', qty=2),
        ViewSize(prod_id='7', size=43, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='8', size=44, price=2000, price_format='2.000грн', qty=1),
    ]
    red_widths = [
        ViewWidth(width='E', sizes=red_E_sizes),
        ViewWidth(width='D', sizes=red_D_sizes),
    ]
    black_E_sizes = [
        ViewSize(prod_id='9', size=38, price=4000, price_format='4.000грн', qty=5),
        ViewSize(prod_id='10', size=39, price=4000, price_format='4.000грн', qty=2),
        ViewSize(prod_id='11', size=40, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='12', size=41, price=4000, price_format='3.000грн', qty=1),
        ViewSize(prod_id='13', size=42, price=4000, price_format='2.000грн', qty=2),

    ]
    black_D_sizes = [
        ViewSize(prod_id='14', size=43, price=2000, price_format='2.000грн', qty=1),
        ViewSize(prod_id='15', size=44, price=2000, price_format='2.000грн', qty=1),
    ]
    black_widths = [
        ViewWidth(width='E', sizes=black_E_sizes),
        ViewWidth(width='D', sizes=black_D_sizes),
    ]
    colors = [
        ViewColor(color='red', widths=red_widths),
        ViewColor(color='black', widths=black_widths),
    ]
    item = ViewShoes(name='Кеды Converse Chuck 70 высокие высокие высокие высокие', colors=colors)
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = ShoesFrame(parent=None, item_pd=item)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec_())
