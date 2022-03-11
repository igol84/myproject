from prjstore.ui.pyside.utils.qt_core import *


class UI_Frame(object):
    def setup_ui(self, parent: QFrame):
        if not parent.objectName():
            parent.setObjectName('ProductPriceEdit')
        self.layuot = QVBoxLayout(parent)

        # Searcher
        self.src_products = QLineEdit()
        self.src_products.setObjectName('ProductLineEdit')

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName('ScrollArea')
        # Product Frame
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_frame.setLayout(self.scroll_layout)
        self.scroll_frame.setObjectName('ProductFrame')

        self.product_frame = QFrame()
        self.scroll_layout.addWidget(self.product_frame)

        self.layout = QVBoxLayout()
        self.product_frame.setLayout(self.layout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.scroll_layout.addItem(self.verticalSpacer)

        # Add to frame layout
        self.scroll.setWidget(self.scroll_frame)

        # Add to layout
        self.layuot.addWidget(self.src_products)
        self.layuot.addWidget(self.scroll)
