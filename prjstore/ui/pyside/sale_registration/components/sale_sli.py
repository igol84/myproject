import sys

from prjstore.ui.pyside.sale_registration.components.sli import SLI_Frame
from prjstore.ui.pyside.sale_registration.schemas import ViewProduct


class SaleSliFrame(SLI_Frame):
    default_color_bg = '#afedc1'
    color_fon_enter = '#E8ffef'

    def mousePressEvent(self, event) -> None:
        pass


if __name__ == "__main__":
    from PySide6.QtWidgets import QVBoxLayout, QApplication, QWidget

    app = QApplication(sys.argv)

    product_pd = ViewProduct(type='product', id='2', price=1600, price_format='1600 грн.', qty=3,
                             name='Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!')
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = SaleSliFrame(parent=None, sli_pd=product_pd)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
