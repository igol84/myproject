from prjstore.ui.pyside.utils.qt_core import *


class UI_PlacesEditor:
    def setup_ui(self, places_editor_frame: QFrame):
        if not places_editor_frame.objectName():
            places_editor_frame.setObjectName('PlacesEditor')
        places_editor_frame.setFixedWidth(260)
        self.layout = QVBoxLayout(places_editor_frame)
        self.layout.setObjectName('VBoxLayout')

        self.handler = QLabel('Место продажи')
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
        self.scroll_frame.setObjectName('PlacesFrame')

        self.places_frame = QFrame()
        self.places_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.layout_places = QVBoxLayout(self.places_frame)

        self.scroll_layout.addWidget(self.places_frame)
        self.scroll_layout.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))

        # Add to frame layout
        self.scroll.setWidget(self.scroll_frame)

        # Add to layout
        self.layout.addWidget(self.handler)
        self.layout.addWidget(self.scroll)
