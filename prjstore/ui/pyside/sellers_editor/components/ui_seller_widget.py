from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class UI_SellerWidget:
    def setup_ui(self, seller_widget: ItemFrame):
        self.item_widget = seller_widget
        seller_widget.setMinimumHeight(seller_widget.height_)
        seller_widget.setFixedWidth(200)
        if not seller_widget.objectName():
            seller_widget.setObjectName('SellerWidget')
        self.layout = QHBoxLayout(seller_widget)
        self.layout.setContentsMargins(10, 2, 10, 2)

        self.label_name = LabelClicked()
        self.label_name.setObjectName('LabelName')
        self.label_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.line_edit_name = LineEdit()
        self.line_edit_name.setObjectName('LineEditName')
        self.line_edit_name.setStyleSheet(f'background-color: #EEE; color: #000')
        self.line_edit_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.line_edit_name.hide()

        self.active_box = QCheckBox()
        self.active_box.setObjectName('BoxActive')
        self.active_box.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add to layout
        self.layout.addWidget(self.label_name)
        self.layout.addWidget(self.line_edit_name)
        self.layout.addWidget(self.active_box)

        self.layout.addLayout(self.layout)


class LabelClicked(QLabel):
    clicked = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        self.clicked.emit()


class LineEdit(QLineEdit):
    escaped = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.escaped.emit()
        QLineEdit.keyPressEvent(self, event)
