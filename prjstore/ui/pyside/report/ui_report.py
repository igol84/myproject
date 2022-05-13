from prjstore.ui.pyside.utils.qt_core import *


class UI_Report:
    def setup_ui(self, report_frame: QFrame):
        if not report_frame.objectName():
            report_frame.setObjectName('ReportPage')
        self.frame = report_frame
        report_frame.setFixedWidth(600)
        report_frame.setMinimumHeight(500)
        self.layout = QVBoxLayout(report_frame)
        self.layout.setObjectName('VBoxLayout')

        self.handler = QLabel('Отчет')
        self.handler.setObjectName('Title')
        self.handler.setAlignment(Qt.AlignCenter)
        self.handler.setStyleSheet('font: 700 17pt "Segue UI"')

        self.menu = QFrame()
        self.menu_layout = QHBoxLayout(self.menu)
        self.menu_layout.setAlignment(Qt.AlignLeft)

        self.combo_box_range = QComboBox()
        self.combo_box_range.setObjectName('ComboBoxRange')
        self.combo_box_range.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.combo_box_place = QComboBox()
        self.combo_box_place.setObjectName('ComboBoxPlace')
        self.combo_box_place.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.menu_layout.addWidget(self.combo_box_range)
        self.menu_layout.addWidget(self.combo_box_place)

        # Scroll Area
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setObjectName('ScrollArea')
        # Report Frame
        self.scroll_frame = QFrame()
        self.scroll_frame.setObjectName('ReportFrame')
        self.scroll_layout = QVBoxLayout(self.scroll_frame)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)

        self.report_frame = QFrame()
        self.report_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout_report = QVBoxLayout(self.report_frame)

        self.scroll_layout.addWidget(self.report_frame)

        # Add to frame layout
        self.scroll.setWidget(self.scroll_frame)

        # Add to layout
        self.layout.addWidget(self.handler)
        self.layout.addWidget(self.menu)
        self.layout.addWidget(self.scroll)

    def setup_dark_style(self):
        self.frame.setStyleSheet(
            '#ReportPage, #ReportFrame {background-color: #2F303B; color: #F8F8F2;}\n'
            '#ReportPage #Title {color: #F8F8F2;}\n'
            'QComboBox, QDateEdit {background-color: #121212; color: #dcdcdc; border:2px solid #484B5E;}\n'
            'QTableWidget {background-color: #2F303B; color: #F8F8F2; selection-background-color: #F8F8F2}\n'
            'QTableWidget {selection-background-color: #F8F8F2; outline: none}\n'
            'QTableWidget::item {background-color: #404252; color: #fff}\n'
            'QTableWidget::item:selected {background-color: #fff; color: #2F303B}\n'
            'QHeaderView {background-color: #2F303B; color: #F8F8F2; gridline-color: #1f1f26;}\n'
            'QHeaderView::section {background-color: #2F303B; color: #F8F8F2; gridline-color: #1f1f26;}\n'
            'QTableWidget QTableCornerButton::section {background-color: #2F303B;}\n'
            'QScrollBar:vertical { border: none; background: rgb(52, 59, 72); width: 8px; margin: 21px 0 21px 0;'
            'border-radius: 0px}\n'
            'QScrollBar::handle:vertical {background: #F8F8F2; min-height: 25px; border-radius: 4px}'
            'QScrollBar::add-line:vertical {border: none; background: rgb(55, 63, 77); height: 20px;'
            'border-bottom-left-radius: 4px; border-bottom-right-radius: 4px; subcontrol-position: bottom;'
            'subcontrol-origin: margin;}\n'
            'QScrollBar::sub-line:vertical {border: none; background: rgb(55, 63, 77); height: 20px;'
            'border-top-left-radius: 4px; border-top-right-radius: 4px; subcontrol-position: top;\n'
            'subcontrol-origin: margin;}'
            'QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical { background: none;}\n'
            'QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }\n'
        )