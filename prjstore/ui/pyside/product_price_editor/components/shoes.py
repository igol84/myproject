from prjstore.ui.pyside.product_price_editor.components.abstract_product import AbstractItem
from prjstore.ui.pyside.product_price_editor.components.shoes_comps import ColorFrame, SizeFrame, ShoesDescFrame
from prjstore.ui.pyside.product_price_editor.components.shoes_comps.shoes_frame_interface import ShoesFrameInterface
from prjstore.ui.pyside.product_price_editor.schemas import ViewShoes, ViewSize, ViewWidth, ViewColor
from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import QHLine, ItemFrame


class ShoesFrame(ItemFrame, AbstractItem, ShoesFrameInterface):
    pr_colors: list[ViewColor]
    __selected_size_frame: SizeFrame

    def __init__(self, parent, item_pd: ViewShoes):
        super().__init__()
        self.setMinimumWidth(300)
        self.__parent_form = parent
        self.__selected_size_frame = None
        self.pr_name = item_pd.name
        self.pr_colors = item_pd.colors
        self.widgets_color: dict[str, ColorFrame] = {}
        self.widgets_h_line: list[QHLine] = []

        layer = QVBoxLayout()
        layer.setContentsMargins(0, 0, 0, 0)
        self.layer_desc = QVBoxLayout()
        self.layer_desc.setContentsMargins(0, 0, 0, 0)
        self.desc_frame = ShoesDescFrame(shoes_frame=self, parent_form=parent)
        self.layer_desc.addWidget(self.desc_frame)
        layer.addLayout(self.layer_desc)
        self.layer_colors = QVBoxLayout()

        for n, view_color in enumerate(self.pr_colors):
            if n:
                h_line = QHLine()
                self.widgets_h_line.append(h_line)
                self.layer_colors.addWidget(h_line)
            color_frame = ColorFrame(shoes_frame=self, pd_color=view_color)
            self.widgets_color[view_color.color] = color_frame
            self.layer_colors.addWidget(color_frame)
        layer.addLayout(self.layer_colors)
        self.setLayout(layer)
        self.hide_colors()

    def get_selected_size_frame(self) -> SizeFrame:
        return self.__selected_size_frame

    def set_selected_size_frame(self, size_frame: SizeFrame) -> None:
        self.desc_frame.selected = False
        if self.__selected_size_frame:
            self.__selected_size_frame.selected = False
        self.pr_id = size_frame.pr_id
        self.__selected_size_frame = size_frame
        self.__selected_size_frame.selected = True
        price_text = self.__selected_size_frame.price
        self.desc_frame.set_price(price_text)
        for color in self.widgets_color.values():
            color.selected = False

    def del_selected_size_frame(self) -> None:
        self.__selected_size_frame = None

    selected_size_frame = property(get_selected_size_frame, set_selected_size_frame, del_selected_size_frame)

    def get_sale_price(self) -> float:
        return self.desc_frame.price_line_edit.text()

    def hide_elements(self):
        self.desc_frame.selected = False
        self.hide_colors()

    def hide_colors(self):
        if self.selected_size_frame and self.selected_size_frame.selected:
            self.selected_size_frame.selected = False
        for color in self.widgets_color.values():
            color.selected = False
            color.hide()
        for h_line in self.widgets_h_line:
            h_line.hide()

    def show_colors(self):
        self.desc_frame.selected = True
        for color in self.widgets_color.values():
            color.show()
        for h_line in self.widgets_h_line:
            h_line.show()

    def __get_parent_form(self):
        return self.__parent_form

    parent_form = property(__get_parent_form)

    def on_press_edit(self):
        if self.parent_form:
            self.parent_form.on_press_edit_by_name(self)

    def edit_size_frame(self, size_frame: SizeFrame) -> None:
        if self.parent_form:
            self.parent_form.on_edit_size(size_frame)

    def on_selected_color(self):
        self.desc_frame.selected = False

    def on_color_edit(self, color_frame):
        if self.parent_form:
            self.parent_form.on_color_edit(color_frame)

    def set_price_of_all_sizes(self, price):
        for color in self.widgets_color.values():
            for width in color.frames_of_width.values():
                for size in width.widgets_of_sizes.values():
                    size.price = price

    def set_new_name(self, name: str):
        self.desc_frame.set_desc(name)


if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QVBoxLayout

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
    item = ViewShoes(name="Кеды Converse Chuck 70 высокие высокие высокие высокие", colors=colors)
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = ShoesFrame(parent=None, item_pd=item)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
