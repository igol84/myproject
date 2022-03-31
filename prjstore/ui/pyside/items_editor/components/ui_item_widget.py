from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class UI_ItemWidget:
    def setup_ui(self, item_widget: ItemFrame):
        self.item_widget = item_widget
        item_widget.setCursor(Qt.PointingHandCursor)
        item_widget.setFixedHeight(item_widget.height_)
        item_widget.setMinimumWidth(500)
        if not item_widget.objectName():
            item_widget.setObjectName('ItemWidget')
        self.layuot = QHBoxLayout(item_widget)
        self.layuot.setObjectName('LayoutItemHBox')
        self.layuot.setContentsMargins(5, 0, 5, 0)

        self.label_prod_id = QLabel()
        self.label_prod_id.setObjectName('LabelProdId')
        self.label_prod_id.setFixedWidth(40)

        self.label_desc = LabelItemDescription(cut=370)
        self.label_desc.setObjectName('LabelDesc')
        self.label_desc.setFixedWidth(80)

        self.spicer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.label_qty = QLabel()
        self.label_qty.setObjectName('LabelGty')
        self.label_qty.setFixedWidth(80)

        self.qty_box = QSpinBox()
        self.qty_box.setObjectName('BoxGty')
        self.qty_box.setStyleSheet(f'background-color: #EEE; color: #000')
        self.qty_box.setRange(0, 100000000)
        self.qty_box.setFixedWidth(80)
        self.qty_box.hide()

        self.label_price_buy = QLabel()
        self.label_price_buy.setObjectName('LabelPriceBuy')
        self.label_price_buy.setFixedWidth(80)

        self.line_edit_price_buy = QLineEdit()
        self.line_edit_price_buy.setObjectName('LineEditPriceBuy')
        self.line_edit_price_buy.setStyleSheet(f'background-color: #EEE; color: #000')
        self.line_edit_price_buy.setFixedWidth(80)
        self.line_edit_price_buy.hide()

        self.label_date_buy = QLabel()
        self.label_date_buy = QLabel()
        self.label_date_buy.setObjectName('LabelDateBuy')
        self.label_date_buy.setFixedWidth(80)

        self.empty_button = QWidget()
        self.empty_button.setObjectName('LabelButton')
        self.empty_button.setFixedWidth(50)

        self.button = QPushButton('del')
        self.button.setStyleSheet(f'background-color: #EEE; color: #000')
        self.button.setObjectName('LabelButton')
        self.button.setFixedWidth(50)
        self.button.hide()

        # Add to layout
        self.layuot.addWidget(self.label_prod_id)
        self.layuot.addWidget(self.label_desc)
        self.layuot.addItem(self.spicer)
        self.layuot.addWidget(self.label_qty)
        self.layuot.addWidget(self.qty_box)
        self.layuot.addWidget(self.label_price_buy)
        self.layuot.addWidget(self.line_edit_price_buy)
        self.layuot.addWidget(self.label_date_buy)
        self.layuot.addWidget(self.button)
        self.layuot.addWidget(self.empty_button)


class LabelItemDescription(QLabel):
    def __init__(self, cut=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cut = cut

    def paintEvent(self, event):
        self.setToolTip(self.text())
        self.setFixedSize(self.parent().width() - self.cut, 20)
        painter = QPainter(self)
        pen = painter.pen()
        painter.setPen(pen)
        metrics = QFontMetrics(self.font())
        pixels_text = metrics.elidedText(self.text(), Qt.ElideRight, self.parent().width() - self.cut)
        self.resize(metrics.size(0, pixels_text).width(), self.parent().height_)
        painter.drawText(self.rect(), self.alignment(), pixels_text)
