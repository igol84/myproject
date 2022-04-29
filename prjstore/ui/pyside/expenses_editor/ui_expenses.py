from prjstore.ui.pyside.utils.pages import PagesFrame
from prjstore.ui.pyside.utils.qt_core import *


class UI_Expenses:
    def setup_ui(self, expenses_frame: QFrame):
        if not expenses_frame.objectName():
            expenses_frame.setObjectName('ExpensesEditor')
        expenses_frame.setFixedWidth(600)
        expenses_frame.setMinimumHeight(700)
        self.layout = QVBoxLayout(expenses_frame)
        self.layout.setObjectName('VBoxLayout')

        self.handler = QLabel('Затраты')
        self.handler.setObjectName('Title')
        self.handler.setAlignment(Qt.AlignCenter)
        self.handler.setStyleSheet('font: 700 17pt "Segue UI"')

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName('ScrollArea')
        # Expenses Frame
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_frame.setObjectName('ExpensesFrame')

        self.expenses_frame = QFrame()
        self.expenses_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout_expenses = QVBoxLayout(self.expenses_frame)

        self.scroll_layout.addWidget(self.expenses_frame)
        self.scroll_layout.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.pages_frame = PagesFrame(parent=expenses_frame)

        # Add to frame layout
        self.scroll.setWidget(self.scroll_frame)

        # Add to layout
        self.layout.addWidget(self.handler)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.pages_frame)


class DelMessageBox(QMessageBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIcon(QMessageBox.Question)
        self.setWindowTitle('Удалить!')
        self.setText('Вы действительно хотите удалить?')
        self.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = self.button(QMessageBox.Yes)
        buttonY.setText('Да')
        buttonN = self.button(QMessageBox.No)
        buttonN.setText('Нет')
