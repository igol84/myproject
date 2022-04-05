import datetime

from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class UI_ItemWidget:
    def setup_ui(self, item_widget: ItemFrame):
        self.item_widget = item_widget
        item_widget.setCursor(Qt.PointingHandCursor)
        item_widget.setMinimumHeight(item_widget.height_)
        item_widget.setMinimumWidth(500)
        if not item_widget.objectName():
            item_widget.setObjectName('ItemWidget')
        self.layout = QVBoxLayout(item_widget)
        self.layout.setContentsMargins(0, 2, 0, 2)

        self.layout_item = QHBoxLayout()
        self.layout_item.setObjectName('LayoutItemHBox')
        self.layout_item.setContentsMargins(0, 0, 0, 0)

        self.label_prod_id = QLabel()
        self.label_prod_id.setObjectName('LabelProdId')
        self.label_prod_id.setFixedWidth(40)

        self.label_desc = LabelItemDescription(cut=370)
        self.label_desc.setObjectName('LabelDesc')
        self.label_desc.setStyleSheet('QToolTip {color: #2F303B; background-color: #F8F8F2;}')
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
        self.label_date_buy.setFixedWidth(60)

        self.empty_button = QWidget()
        self.empty_button.setObjectName('LabelButton')
        self.empty_button.setFixedWidth(70)

        self.button_edit = QPushButton('ok')
        self.button_edit.setStyleSheet(f'background-color: #EEE; color: #000')
        self.button_edit.setObjectName('LabelButton')
        self.button_edit.setFixedWidth(30)
        self.button_edit.hide()

        self.button_del = QPushButton('del')
        self.button_del.setStyleSheet(f'background-color: #EEE; color: #000')
        self.button_del.setObjectName('LabelButton')
        self.button_del.setFixedWidth(35)
        self.button_del.hide()

        # Add to layout
        self.layout_item.addWidget(self.label_prod_id)
        self.layout_item.addWidget(self.label_desc)
        self.layout_item.addItem(self.spicer)
        self.layout_item.addWidget(self.label_qty)
        self.layout_item.addWidget(self.qty_box)
        self.layout_item.addWidget(self.label_price_buy)
        self.layout_item.addWidget(self.line_edit_price_buy)
        self.layout_item.addWidget(self.label_date_buy)
        self.layout_item.addWidget(self.button_edit)
        self.layout_item.addWidget(self.button_del)
        self.layout_item.addWidget(self.empty_button)

        self.list_sales = ListWidget()

        self.layout.addLayout(self.layout_item)
        self.layout.addWidget(self.list_sales)


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


class ListWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet(f'background-color: #EEE; color: #000')
        self.setCursor(Qt.ArrowCursor)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setContentsMargins(0, 0, 5, 0)
        self.setMaximumHeight(90)
        self.setCursor(Qt.PointingHandCursor)
        self.hide()


class WidgetItem(QListWidgetItem):
    def __init__(self, text: str, date: datetime.date, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setText(text)
        self.setData(Qt.UserRole, date)
