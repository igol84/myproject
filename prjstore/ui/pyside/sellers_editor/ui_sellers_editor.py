from prjstore.ui.pyside.utils.pages import PagesFrame
from prjstore.ui.pyside.utils.qt_core import *


class UI_SellersEditor:
    def setup_ui(self, sellers_editor_frame: QFrame):
        if not sellers_editor_frame.objectName():
            sellers_editor_frame.setObjectName('SellersEditor')
        sellers_editor_frame.setFixedWidth(260)
        self.layout = QVBoxLayout(sellers_editor_frame)
        self.layout.setObjectName('VBoxLayout')

        self.handler = QLabel('Прдавцы')
        self.handler.setAlignment(Qt.AlignCenter)
        self.handler.setStyleSheet('font: 700 17pt "Segue UI"')

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName('ScrollArea')
        # Product Frame
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_frame.setObjectName('SellersFrame')

        self.sellers_frame = QFrame()
        self.sellers_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout_sellers = QVBoxLayout(self.sellers_frame)

        self.scroll_layout.addWidget(self.sellers_frame)
        self.scroll_layout.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.pages_frame = PagesFrame(parent=sellers_editor_frame)

        # Add to frame layout
        self.scroll.setWidget(self.scroll_frame)

        # Add to layout
        self.layout.addWidget(self.handler)
        self.layout.addWidget(self.scroll)
        self.layout.addWidget(self.pages_frame)
