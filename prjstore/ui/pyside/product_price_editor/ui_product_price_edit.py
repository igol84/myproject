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
        self.product_layout = QFrame()
        self.frame_layout = QVBoxLayout()
        self.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.frame_layout.setSpacing(0)
        self.product_layout.setLayout(self.frame_layout)
        self.product_layout.setObjectName('ProductFrame')

        self.product_frame = QFrame()
        self.frame_layout.addWidget(self.product_frame)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.frame_layout.addItem(self.verticalSpacer)

        # Add to frame layout
        self.scroll.setWidget(self.product_layout)

        # Add to layout
        self.layuot.addWidget(self.src_products)
        self.layuot.addWidget(self.scroll)
