# IMPORT CUSTOM WIDGETS
from prjstore.ui.pyside.utils.push_button import PyPushBottom
from prjstore.ui.pyside.utils.qt_core import *


class UI_MainWindow(object):
    def setup_ui(self, parent: QMainWindow):
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
        self.toggle_button = PyPushBottom(text='', icon_path='icon_menu.svg', icon_color='green')
        self.btn_price_editor = PyPushBottom(text='Редактор товаров', icon_path='icon_product_price_editor.svg')
        self.btn_new_items = PyPushBottom(text='Новый товар', icon_path='icon_new_items.svg', is_active=True)
        self.btn_sale = PyPushBottom(text='Продажа', icon_path='icon_sale.svg')
        self.btn_sellers = PyPushBottom(text='Продавцы', icon_path='icon_seller.svg')
        self.btn_expenses = PyPushBottom(text='Затраты', icon_path='icon_expenses.svg')
        self.btn_report = PyPushBottom(text='Отчет', icon_path='icon_report.svg')

        # ADD BUTTONS TO LAYOUT
        self.left_menu_top_layout.addWidget(self.toggle_button)
        self.left_menu_top_layout.addWidget(self.btn_new_items)
        self.left_menu_top_layout.addWidget(self.btn_price_editor)
        self.left_menu_top_layout.addWidget(self.btn_sale)
        self.left_menu_top_layout.addWidget(self.btn_sellers)
        self.left_menu_top_layout.addWidget(self.btn_expenses)
        self.left_menu_top_layout.addWidget(self.btn_report)

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
        self.login_button = PyPushBottom(text='Login', icon_path='icon_login.svg')
        self.settings_button = PyPushBottom(text='Settings', icon_path='icon_settings.svg')

        # ADD BUTTONS TO LAYOUT
        self.left_menu_bottom_layout.addWidget(self.login_button)
        self.left_menu_bottom_layout.addWidget(self.settings_button)

        # LABEL VERSION
        # //////////////////////////////////////////////////////////////////
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
        self.top_label_left = QLabel('')

        # top spicer
        self.top_spacer = QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        # right label
        self.top_label_right = QLabel('')
        self.top_label_right.setStyleSheet('font: 700 9pt "Segue UI"')

        # Add to layout
        self.top_bar_layout.addWidget(self.top_label_left)
        self.top_bar_layout.addItem(self.top_spacer)
        self.top_bar_layout.addWidget(self.top_label_right)

        # application pages
        self.pages = QStackedWidget()
        self.pages.setObjectName(u"StackedWidget")
        self.pages.setStyleSheet('#StackedWidget {background-color: #2F303B;}')

        # =================== Settings page ===================
        self.page_settings = QWidget()
        self.page_settings.setObjectName(u"page_3")
        self.verticalLayout_4 = QVBoxLayout(self.page_settings)
        self.verticalLayout_4.setObjectName(u"verticalLayout")
        self.label = QLabel(self.page_settings)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignCenter)
        self.verticalLayout_4.addWidget(self.label)
        self.pages.addWidget(self.page_settings)

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

    def setup_login_module(self, module):
        self.page_login_form = QFrame()
        layout = QVBoxLayout(self.page_login_form)
        login_frame = module
        layout.addWidget(login_frame)
        self.pages.addWidget(self.page_login_form)

    def setup_sale_module(self, module):
        self.page_sale_form = module
        self.pages.addWidget(self.page_sale_form)

    def setup_price_editor(self, module):
        self.price_editor_form = module
        self.price_editor_form.setMaximumWidth(600)
        self.price_editor_form.setMinimumWidth(600)
        self.pages.addWidget(self.price_editor_form)

    def setup_expenses_module(self, module):
        self.page_expenses_form = module
        self.pages.addWidget(self.page_expenses_form)

    def setup_report_module(self, module):
        self.page_report = module
        self.pages.addWidget(self.page_report)

    def setup_sellers_and_places_module(self, sellers_form, places_form):
        sellers_form = sellers_form
        sellers_form.setObjectName(u"SellersForm")

        places_form = places_form
        places_form.setObjectName(u"PlacesForm")

        self.sellers_and_places_form = QFrame()
        layout = QHBoxLayout(self.sellers_and_places_form)
        layout.addWidget(sellers_form)
        layout.addWidget(places_form)
        layout.addItem(QSpacerItem(0, 100, QSizePolicy.Expanding, QSizePolicy.Expanding))

        self.pages.addWidget(self.sellers_and_places_form)

    def setup_items_form(self, new_items_module, items_module):
        new_items_form = new_items_module
        new_items_form.setMaximumWidth(340)
        new_items_form.setObjectName(u"NewItemsForm")

        edit_items_form = items_module
        edit_items_form.setObjectName(u"EditItemsForm")

        self.items_form = QFrame()
        layout = QHBoxLayout(self.items_form)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(new_items_form)
        layout.addWidget(edit_items_form)

        self.pages.addWidget(self.items_form)
