from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class UI_AddExpenseWidget:
    def setup_ui(self, expense_widget: ItemFrame):
        expense_widget.setMinimumHeight(expense_widget.height_)
        if not expense_widget.objectName():
            expense_widget.setObjectName('SellerWidget')
        self.layout = QHBoxLayout(expense_widget)
        self.layout.setContentsMargins(10, 2, 10, 2)

        self.combo_box_places = QComboBox()
        self.combo_box_places.setObjectName('ComboBoxPlaces')
        self.combo_box_places.setStyleSheet(f'background-color: #fff; color: #000')
        self.combo_box_places.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.line_edit_desc = LineEdit()
        self.line_edit_desc.setObjectName('LineEditDesc')
        self.line_edit_desc.setStyleSheet(f'background-color: #fff; color: #000')
        self.line_edit_desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.date_edit = QDateEdit()
        self.date_edit.setObjectName('DateEdit')
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setStyleSheet(f'background-color: #fff; color: #000')
        self.date_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.line_edit_cost = LineEdit()
        self.line_edit_cost.setObjectName('LineEditCost')
        self.line_edit_cost.setStyleSheet(f'background-color: #fff; color: #000')
        validator_reg = QRegularExpressionValidator(QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.line_edit_cost.setValidator(validator_reg)
        self.line_edit_cost.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.btn_add = QPushButton('+')
        self.btn_add.setFixedWidth(30)
        self.btn_add.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Add to layout
        self.layout.addWidget(self.combo_box_places)
        self.layout.addWidget(self.line_edit_desc)
        self.layout.addWidget(self.date_edit)
        self.layout.addWidget(self.line_edit_cost)
        self.layout.addWidget(self.btn_add)


class LineEdit(QLineEdit):
    escaped = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.escaped.emit()
        QLineEdit.keyPressEvent(self, event)
