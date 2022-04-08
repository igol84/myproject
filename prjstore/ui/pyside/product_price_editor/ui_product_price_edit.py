from prjstore.ui.pyside.utils.qt_core import *


class UI_Frame(object):
    def setup_ui(self, parent: QFrame):
        if not parent.objectName():
            parent.setObjectName('ProductPriceEdit')
        self.layout = QVBoxLayout(parent)
        self.layout.setObjectName('VBoxLayout')

        # Searcher
        self.src_products = QLineEdit()
        self.src_products.setObjectName('ProductLineEdit')
        self.src_products.setClearButtonEnabled(True)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName('ScrollArea')
        # Product Frame
        self.scroll_frame = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_frame.setObjectName('ProductFrame')

        self.product_frame = QFrame()
        self.product_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout_products = QVBoxLayout(self.product_frame)

        self.scroll_layout.addWidget(self.product_frame)
        self.scroll_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Add to frame layout
        self.scroll.setWidget(self.scroll_frame)

        # Add to layout
        self.layout.addWidget(self.src_products)
        self.layout.addWidget(self.scroll)
