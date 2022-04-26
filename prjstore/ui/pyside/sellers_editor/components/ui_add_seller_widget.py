from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class UI_AddSellerWidget:
    def setup_ui(self, seller_widget: ItemFrame):
        seller_widget.setMinimumHeight(seller_widget.height_)
        seller_widget.setFixedWidth(200)
        if not seller_widget.objectName():
            seller_widget.setObjectName('SellerWidget')
        self.layout = QHBoxLayout(seller_widget)
        self.layout.setContentsMargins(10, 2, 10, 2)

        self.line_edit_name = LineEdit()
        self.line_edit_name.setObjectName('LineEditName')
        self.line_edit_name.setStyleSheet(f'background-color: #EEE; color: #000')
        self.line_edit_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.btn_add = QPushButton('+')
        self.btn_add.setFixedWidth(30)
        self.btn_add.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add to layout
        self.layout.addWidget(self.line_edit_name)
        self.layout.addWidget(self.btn_add)


class LineEdit(QLineEdit):
    escaped = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.escaped.emit()
        QLineEdit.keyPressEvent(self, event)
