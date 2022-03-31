from prjstore.ui.pyside.utils.qt_core import *


class UI_ItemsEditor:
    def setup_ui(self, items_editor_frame: QFrame):
        if not items_editor_frame.objectName():
            items_editor_frame.setObjectName('ItemsEditor')
        items_editor_frame.resize(500, 600)
        items_editor_frame.setMinimumWidth(600)
        self.layout = QVBoxLayout(items_editor_frame)
        self.layout.setObjectName('VBoxLayout')

        # Searcher
        self.src_items = QLineEdit()
        self.src_items.setObjectName('LineEditStcItems')

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

        self.layout_items = QVBoxLayout(self.product_frame)

        self.scroll_layout.addWidget(self.product_frame)
        self.scroll_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Add to frame layout
        self.scroll.setWidget(self.scroll_frame)

        # Add to layout
        self.layout.addWidget(self.src_items)
        self.layout.addWidget(self.scroll)
