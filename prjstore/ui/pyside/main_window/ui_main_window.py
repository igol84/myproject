from prjstore.ui.pyside.qt_core import *

# IMPORT CUSTOM WIDGETS
from prjstore.ui.pyside.utils.push_button import PyPushBottom


class UI_MainWindow(object):
    def setup_ui(self, parent: QMainWindow, pages: list):
        if not parent.objectName():
            parent.setObjectName('MainWindow')

        # SET INITIAL PARAMETERS
        # //////////////////////////////////////////////////////////////////
        parent.resize(1200, 720)
        parent.setMinimumSize(960, 540)

        # CREATE CENTRAL WIDGET
        # //////////////////////////////////////////////////////////////////
        self.central_frame = QFrame()

        # CREATE MAIN LAYOUT
        self.main_layout = QHBoxLayout(self.central_frame)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # LEFT MENU
        # //////////////////////////////////////////////////////////////////
        self.left_menu = QFrame()
        self.left_menu.setStyleSheet('background-color: #484B5E')
        self.left_menu.setMinimumWidth(50)
        self.left_menu.setMaximumWidth(50)

        # LEFT MENU LAYOUT
        self.left_menu_layout = QVBoxLayout(self.left_menu)
        self.left_menu_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_layout.setSpacing(0)

        # TOP FRAME MENU
        self.left_menu_top_frame = QFrame()
        self.left_menu_top_frame.setObjectName('left_menu_top_frame')
        self.left_menu_top_frame.setMinimumHeight(40)

        # TOP FRAME LAYOUT
        self.left_menu_top_layout = QVBoxLayout(self.left_menu_top_frame)
        self.left_menu_top_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_top_layout.setSpacing(0)

        # TOP BUTTONS
        self.toggle_button = PyPushBottom(text='Toggle', icon_path='icon_menu.svg', icon_color='green')
        self.btn_1 = PyPushBottom(text='Page 1', icon_path='icon_new_items.svg', is_active=True)
        self.btn_2 = PyPushBottom(text='Page 2', icon_path='icon_sale.svg')

        # ADD BUTTONS TO LAYOUT
        self.left_menu_top_layout.addWidget(self.toggle_button)
        self.left_menu_top_layout.addWidget(self.btn_1)
        self.left_menu_top_layout.addWidget(self.btn_2)

        # MENU SPICER
        # //////////////////////////////////////////////////////////////////
        self.left_menu_spacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)

        # BOTTOM FRAME MENU
        # //////////////////////////////////////////////////////////////////
        self.left_menu_bottom_frame = QFrame()
        self.left_menu_bottom_frame.setObjectName('left_menu_bottom_frame')
        self.left_menu_bottom_frame.setMinimumHeight(40)

        # BOTTOM FRAME LAYOUT
        self.left_menu_bottom_layout = QVBoxLayout(self.left_menu_bottom_frame)
        self.left_menu_bottom_layout.setContentsMargins(0, 0, 0, 0)
        self.left_menu_bottom_layout.setSpacing(0)

        # BOTTOM BUTTONS
        self.settings_button = PyPushBottom(text='Settings', icon_path='icon_settings.svg')

        # ADD BUTTONS TO LAYOUT
        self.left_menu_bottom_layout.addWidget(self.settings_button)

        # LABEL VERSION
        self.left_menu_label_version = QLabel('v1.0')
        self.left_menu_label_version.setAlignment(Qt.AlignLeft)
        self.left_menu_label_version.setMinimumHeight(30)
        self.left_menu_label_version.setMaximumHeight(30)
        self.left_menu_label_version.setStyleSheet('color: #C3CCDF; margin-left: 5px; margin-top: 5px')

        # ADD To LAYOUT
        self.left_menu_layout.addWidget(self.left_menu_top_frame)
        self.left_menu_layout.addItem(self.left_menu_spacer)
        self.left_menu_layout.addWidget(self.left_menu_bottom_frame)
        self.left_menu_layout.addWidget(self.left_menu_label_version)

        # CONTENT
        # //////////////////////////////////////////////////////////////////
        self.content = QFrame()
        # self.content.setStyleSheet('. {background-color: #2F303B}')

        # content layout
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        # TOP BAR
        self.top_bar = QFrame()
        self.top_bar.setMinimumHeight(30)
        self.top_bar.setMaximumHeight(30)
        self.top_bar.setStyleSheet('background-color: #21232D; color: #6272A4')
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(10, 0, 10, 0)

        # left label
        self.top_label_left = QLabel('left text')

        # top spicer
        self.top_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # right label
        self.top_label_right = QLabel('right text')
        self.top_label_right.setStyleSheet('font: 700 9pt "Segue UI"')

        # Add to layout
        self.top_bar_layout.addWidget(self.top_label_left)
        self.top_bar_layout.addItem(self.top_spacer)
        self.top_bar_layout.addWidget(self.top_label_right)

        # application pages
        self.pages = QStackedWidget()
        self.pages.setObjectName(u"SaleForm")
        self.pages.setStyleSheet('#SaleForm {background-color: #2F303B;}')



        self.page_1 = pages['items_form']
        self.page_1.setMaximumWidth(340)
        self.page_1.setMinimumWidth(340)
        self.page_1.setObjectName(u"page_2")
        self.pages.addWidget(self.page_1)

        self.page_2 = pages['sale_form']
        self.pages.addWidget(self.page_2)

        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout = QVBoxLayout(self.page_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.page_3)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.pages.addWidget(self.page_3)
        self.pages.setCurrentWidget(self.page_3)

        # BOTTOM BAR
        self.bottom_bar = QFrame()
        self.bottom_bar.setMinimumHeight(30)
        self.bottom_bar.setMaximumHeight(30)
        self.bottom_bar.setStyleSheet('background-color: #21232D; color: #6272A4')

        self.bottom_bar_layout = QHBoxLayout(self.bottom_bar)
        self.bottom_bar_layout.setContentsMargins(10, 0, 10, 0)

        # left label
        self.bottom_label_left = QLabel('bottom left')

        # top spicer
        self.bottom_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # right label
        self.bottom_label_right = QLabel('@ 2022')

        # Add to layout
        self.bottom_bar_layout.addWidget(self.bottom_label_left)
        self.bottom_bar_layout.addItem(self.bottom_spacer)
        self.bottom_bar_layout.addWidget(self.bottom_label_right)

        # add content layout
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.pages)
        self.content_layout.addWidget(self.bottom_bar)

        self.main_layout.addWidget(self.left_menu)
        self.main_layout.addWidget(self.content)

        parent.setCentralWidget(self.central_frame)

        self.toggle_button.clicked.connect(self.animation_button)

    def animation_button(self):
        menu_width = self.left_menu.width()
        width = 50
        if menu_width == 50:
            width = 240

        # start animation
        self.animation = QPropertyAnimation(self.left_menu, b'minimumWidth')
        self.animation.setStartValue(menu_width)
        self.animation.setEndValue(width)
        self.animation.setDuration(500)
        self.animation.setEasingCurve(QEasingCurve.InOutCirc)
        self.animation.start()
