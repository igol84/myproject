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

        # Add to frame layout
        self.scroll.setWidget(self.scroll_frame)

        # Add to layout
        self.layout.addWidget(self.handler)
        self.layout.addWidget(self.scroll)
