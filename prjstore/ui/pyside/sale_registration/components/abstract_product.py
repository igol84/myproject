from PySide2.QtWidgets import QFrame


class ItemFrame(QFrame):
    default_color_bg = '#E1E1E1'
    default_color_text = '#000'
    color_fon_on_enter = '#CCC'
    current_color_bg = '#1287A8'
    current_color_text = '#fff'
    height_ = 30
    width_ = 300
    font_family = 'Times'
    font_size = 10

    def __init__(self):
        super().__init__()
        self.adjustSize()
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.color_fon = self.default_color_bg
        self.color_text = self.default_color_text


class Item:
    pr_id: str
    pr_price: float
    pr_qty: int

    def get_sale_price(self) -> float:
        ...

    def get_sale_qty(self) -> int:
        ...
