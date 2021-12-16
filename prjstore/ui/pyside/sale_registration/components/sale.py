import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget, QApplication, QLabel

from prjstore.ui.pyside.sale_registration.components.sale_sli import SaleSliFrame
from prjstore.ui.pyside.sale_registration.schemas import ViewSale, ViewProduct, ViewSeller, ViewPlace


class Sale_Frame(QWidget):
    sale_id: int
    place: ViewPlace
    seller: ViewSeller
    products: list[ViewProduct]

    def __init__(self, parent, view_sale: ViewSale):
        super().__init__()
        self.__parent_form = parent
        self.sale_id = view_sale.id
        self.place = view_sale.place
        self.seller = view_sale.seller
        self.products = view_sale.products
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        label = QLabel(f'{self.place.desc} - {self.seller.desc}')
        label.setStyleSheet('font-size: 12pt; background-color: #b3a9fc;')
        layout.addWidget(label)
        for sli in self.products:
            widget = SaleSliFrame(parent=self.__parent_form, sli_pd=sli)
            layout.addWidget(widget)
        self.setLayout(layout)

    def __get_parent_form(self) -> object:
        return self.__parent_form

    parent_form = property(__get_parent_form)


if __name__ == "__main__":
    from PySide6.QtWidgets import QVBoxLayout

    app = QApplication(sys.argv)
    place = ViewPlace(id=1, desc='Box')
    seller = ViewSeller(id=1, desc='Igor')
    product_pd_1 = ViewProduct(type='product', prod_id='2', price=1600, price_format='1600 грн.', qty=3,
                               name='Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!')
    product_pd_2 = ViewProduct(type='product', prod_id='3', price=600, price_format='600 грн.', qty=2,
                               name='Кроссовки Adidas красные')
    sale_pd = ViewSale(id=1, place=place, seller=seller, products=[product_pd_1, product_pd_2])
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = Sale_Frame(parent=None, view_sale=sale_pd)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
