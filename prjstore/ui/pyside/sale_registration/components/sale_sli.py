import sys

from prjstore.ui.pyside.sale_registration.components.sli import SLI_Frame
from prjstore.ui.pyside.sale_registration.schemas import ViewProduct


class SaleSliFrame(SLI_Frame):
    default_color_bg = '#afedc1'
    color_fon_enter = '#E8ffef'

    def on_pressed_price_line_edit(self):
        new_price = float(self.price_edit.text())
        sale_id = self.parent().sale_id
        self.parent_form.edit_sale_price_in_sli(self.sli_product_id, self.sli_price, new_price, sale_id)
        self.parent_form.selected_sli_widget = None
        self.update()

    def on_push_button_plus(self):
        if self.parent_form:
            self.parent_form.put_item_form_sli_to_items(sale_id=self.parent().sale_id)
        self.update()


if __name__ == "__main__":
    from PySide6.QtWidgets import QVBoxLayout, QApplication, QWidget

    app = QApplication(sys.argv)

    product_pd = ViewProduct(type='product', prod_id='2', price=1600, price_format='1600 грн.', qty=3,
                             name='Кроссовки Adidas Y-1 красные, натуральная замша. Топ качество!')
    win = QWidget()
    v_box = QVBoxLayout(win)
    frame = SaleSliFrame(parent=None, sli_pd=product_pd)
    v_box.addWidget(frame)
    win.show()
    sys.exit(app.exec())
