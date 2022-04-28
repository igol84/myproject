from prjstore.ui.pyside.utils.qt_core import *
from prjstore.ui.pyside.utils.widgets import ItemFrame


class UI_ExpenseWidget:
    def setup_ui(self, expense_widget: ItemFrame):
        self.expense_widget = expense_widget
        expense_widget.setCursor(Qt.PointingHandCursor)
        expense_widget.setMinimumHeight(expense_widget.height_)
        if not expense_widget.objectName():
            expense_widget.setObjectName('ExpenseWidget')
        self.layout = QHBoxLayout(expense_widget)
        self.layout.setContentsMargins(10, 2, 10, 2)

        # ================= Place =======================
        self.label_place = QLabel()
        self.label_place.setObjectName('LabelPlace')
        self.label_place.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.combo_box_place = QComboBox()
        self.combo_box_place.addItem('')
        self.combo_box_place.setObjectName('ComboBoxPlace')
        self.combo_box_place.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.combo_box_place.hide()

        self.layout.addWidget(self.label_place)
        self.layout.addWidget(self.combo_box_place)

        # ================= Desc =======================
        self.label_desc = QLabel()
        self.label_desc.setObjectName('LabelDesc')
        self.label_desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.line_edit_desc = LineEdit()
        self.line_edit_desc.setObjectName('LineEditName')
        self.line_edit_desc.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.line_edit_desc.hide()

        self.layout.addWidget(self.label_desc)
        self.layout.addWidget(self.line_edit_desc)

        # ================= Date =======================
        self.label_date = QLabel()
        self.label_date.setObjectName('LabelDate')
        self.label_date.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.date_edit = QDateEdit()
        self.date_edit.setObjectName('DateEdit')
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.date_edit.hide()

        self.layout.addWidget(self.label_date)
        self.layout.addWidget(self.date_edit)

        # ================= Cost =======================
        self.label_cost = QLabel()
        self.label_cost.setObjectName('LabelCost')
        self.label_cost.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.line_edit_cost = LineEdit()
        self.line_edit_cost.setObjectName('LineEditCost')
        validator_reg = QRegularExpressionValidator(QRegularExpression("[0-9]{1,7}[.]*[0-9]{0,2}"))
        self.line_edit_cost.setValidator(validator_reg)
        self.line_edit_cost.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.line_edit_cost.hide()

        self.layout.addWidget(self.label_cost)
        self.layout.addWidget(self.line_edit_cost)

        # ================= Button Ok =======================
        self.btn_ok = QPushButton('ok')
        self.btn_ok.setFixedWidth(30)
        self.btn_ok.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_ok.hide()

        self.layout.addWidget(self.btn_ok)

        # ================= Button Del =======================
        self.btn_del = QPushButton('X')
        self.btn_del.setFixedWidth(30)
        self.btn_del.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btn_del.hide()

        self.layout.addWidget(self.btn_del)


class LineEdit(QLineEdit):
    escaped = Signal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Escape:
            self.escaped.emit()
        QLineEdit.keyPressEvent(self, event)
