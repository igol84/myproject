# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'sale_registrationuaQZYh.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################
from ..qt_core import *


class Ui_Form(object):
    def setupUi(self, SaleForm):
        if not SaleForm.objectName():
            SaleForm.setObjectName(u"SaleForm")
        SaleForm.setWindowModality(Qt.WindowModal)
        SaleForm.resize(1064, 796)
        self.verticalLayout_2 = QVBoxLayout(SaleForm)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.title = QLabel(SaleForm)
        self.title.setObjectName(u"title")
        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)

        self.verticalLayout_2.addWidget(self.title)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget_area = QWidget(SaleForm)
        self.widget_area.setObjectName(u"widget_area")
        self.horizontalLayout = QHBoxLayout(self.widget_area)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sale = QWidget(self.widget_area)
        self.sale.setObjectName(u"sale")
        self.verticalLayout_6 = QVBoxLayout(self.sale)
        self.verticalLayout_6.setSpacing(9)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.gridLayout.setHorizontalSpacing(4)
        self.gridLayout.setVerticalSpacing(6)
        self.label = QLabel(self.sale)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.label_2 = QLabel(self.sale)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)

        self.combo_box_place_of_sale = QComboBox(self.sale)
        self.combo_box_place_of_sale.setObjectName(u"combo_box_place_of_sale")

        self.gridLayout.addWidget(self.combo_box_place_of_sale, 1, 1, 1, 1)

        self.date_edit = QDateEdit(self.sale)
        self.date_edit.setObjectName(u"date_edit")
        self.date_edit.setCalendarPopup(True)

        self.gridLayout.addWidget(self.date_edit, 0, 1, 1, 1)

        self.combo_box_seller = QComboBox(self.sale)
        self.combo_box_seller.setObjectName(u"combo_box_seller")

        self.gridLayout.addWidget(self.combo_box_seller, 2, 1, 1, 1)

        self.label_3 = QLabel(self.sale)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)

        self.verticalLayout_6.addLayout(self.gridLayout)

        self.scroll_slis = QScrollArea(self.sale)
        self.scroll_slis.setObjectName(u"scroll_slis")
        font1 = QFont()
        font1.setBold(False)
        self.scroll_slis.setFont(font1)
        self.scroll_slis.setWidgetResizable(True)
        self.widget_slis = QWidget()
        self.widget_slis.setObjectName(u"widget_slis")
        self.widget_slis.setGeometry(QRect(0, 0, 508, 605))
        self.sli_layout = QVBoxLayout(self.widget_slis)
        self.sli_layout.setObjectName(u"sli_layout")
        self.scroll_slis.setWidget(self.widget_slis)

        self.verticalLayout_6.addWidget(self.scroll_slis)

        self.horizontalLayout.addWidget(self.sale)

        self.items = QWidget(self.widget_area)
        self.items.setObjectName(u"items")
        self.verticalLayout_3 = QVBoxLayout(self.items)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 29, 0, 0)
        self.frame = QFrame(self.items)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(16777215, 100))
        self.frame.setSizeIncrement(QSize(0, 0))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.frame)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.title_items = QLabel(self.frame)
        self.title_items.setObjectName(u"title_items")
        font2 = QFont()
        font2.setPointSize(11)
        self.title_items.setFont(font2)
        self.title_items.setMargin(0)
        self.title_items.setIndent(1)

        self.verticalLayout_7.addWidget(self.title_items)

        self.src_items = QLineEdit(self.frame)
        self.src_items.setObjectName(u"src_items")
        self.src_items.setClearButtonEnabled(True)

        self.verticalLayout_7.addWidget(self.src_items)

        self.verticalLayout_3.addWidget(self.frame)

        self.scroll_items = QScrollArea(self.items)
        self.scroll_items.setObjectName(u"scroll_items")
        self.scroll_items.setWidgetResizable(True)
        self.widget_items = QWidget()
        self.widget_items.setObjectName(u"widget_items")
        self.widget_items.setGeometry(QRect(0, 0, 508, 609))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_items.sizePolicy().hasHeightForWidth())
        self.widget_items.setSizePolicy(sizePolicy)
        self.items_layout = QVBoxLayout(self.widget_items)
        self.items_layout.setObjectName(u"items_layout")
        self.items_layout.setContentsMargins(5, 5, 5, 5)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.items_layout.addItem(self.verticalSpacer)

        self.scroll_items.setWidget(self.widget_items)

        self.verticalLayout_3.addWidget(self.scroll_items)

        self.horizontalLayout.addWidget(self.items)

        self.verticalLayout.addWidget(self.widget_area)

        self.total = QLabel(SaleForm)
        self.total.setObjectName(u"total")
        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(False)
        self.total.setFont(font3)
        self.total.setStyleSheet(u"margin-left: 15px")
        self.total.setWordWrap(False)

        self.verticalLayout.addWidget(self.total)

        self.buttonBox = QDialogButtonBox(SaleForm)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.NoButton)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(SaleForm)

        QMetaObject.connectSlotsByName(SaleForm)

    # setupUi

    def retranslateUi(self, SaleForm):
        SaleForm.setWindowTitle(QCoreApplication.translate("Form",
                                                           u"\u041f\u0440\u043e\u0434\u0430\u0436\u0430 \u0442\u043e\u0432\u0430\u0440\u0430",
                                                           None))
        self.title.setText(QCoreApplication.translate("Form",
                                                      u"\u041e\u0444\u043e\u0440\u043c\u043b\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u0434\u0430\u0436",
                                                      None))
        self.label.setText(
            QCoreApplication.translate("Form", u"\u0413\u0434\u0435 \u043f\u0440\u043e\u0434\u0430\u043b\u0438", None))
        self.label_2.setText(
            QCoreApplication.translate("Form", u"\u041a\u0442\u043e \u043f\u0440\u043e\u0434\u0430\u043b", None))
        self.label_3.setText(
            QCoreApplication.translate("Form", u"\u0414\u0430\u0442\u0430 \u043f\u0440\u043e\u0434\u0430\u0436\u0438",
                                       None))
        self.title_items.setText(QCoreApplication.translate("Form", u"\u0422\u043e\u0432\u0430\u0440\u044b", None))
        self.total.setText("")
    # retranslateUi
