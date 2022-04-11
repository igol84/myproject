# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'itemiGfGhG.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from prjstore.ui.pyside.utils.qt_core import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(660, 656)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setLayoutDirection(Qt.LeftToRight)
        self.verticalLayout_3 = QVBoxLayout(Dialog)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.verticalLayout_3.addWidget(self.frame)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.qty_label = QLabel(Dialog)
        self.qty_label.setObjectName(u"qty_label")

        self.gridLayout.addWidget(self.qty_label, 3, 2, 1, 1)

        self.price_line_edit = QLineEdit(Dialog)
        self.price_line_edit.setObjectName(u"price_line_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.price_line_edit.sizePolicy().hasHeightForWidth())
        self.price_line_edit.setSizePolicy(sizePolicy1)
        self.price_line_edit.setMinimumSize(QSize(70, 0))
        self.price_line_edit.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.price_line_edit, 1, 3, 1, 1)

        self.type_combo_box = QComboBox(Dialog)
        self.type_combo_box.addItem("")
        self.type_combo_box.addItem("")
        self.type_combo_box.setObjectName(u"type_combo_box")
        sizePolicy1.setHeightForWidth(self.type_combo_box.sizePolicy().hasHeightForWidth())
        self.type_combo_box.setSizePolicy(sizePolicy1)
        self.type_combo_box.setEditable(False)

        self.gridLayout.addWidget(self.type_combo_box, 3, 1, 1, 1)

        self.type_label = QLabel(Dialog)
        self.type_label.setObjectName(u"type_label")

        self.gridLayout.addWidget(self.type_label, 3, 0, 1, 1)

        self.price_label = QLabel(Dialog)
        self.price_label.setObjectName(u"price_label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.price_label.sizePolicy().hasHeightForWidth())
        self.price_label.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.price_label, 1, 2, 1, 1)

        self.buy_price_line_edit = QLineEdit(Dialog)
        self.buy_price_line_edit.setObjectName(u"buy_price_line_edit")
        sizePolicy1.setHeightForWidth(self.buy_price_line_edit.sizePolicy().hasHeightForWidth())
        self.buy_price_line_edit.setSizePolicy(sizePolicy1)
        self.buy_price_line_edit.setMinimumSize(QSize(70, 0))
        self.buy_price_line_edit.setMaximumSize(QSize(70, 16777215))

        self.gridLayout.addWidget(self.buy_price_line_edit, 1, 1, 1, 1)

        self.name_label = QLabel(Dialog)
        self.name_label.setObjectName(u"name_label")
        sizePolicy2.setHeightForWidth(self.name_label.sizePolicy().hasHeightForWidth())
        self.name_label.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.name_label, 0, 0, 1, 1)

        self.buy_price_label = QLabel(Dialog)
        self.buy_price_label.setObjectName(u"buy_price_label")
        sizePolicy2.setHeightForWidth(self.buy_price_label.sizePolicy().hasHeightForWidth())
        self.buy_price_label.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.buy_price_label, 1, 0, 1, 1)

        self.qty_spin_box = QSpinBox(Dialog)
        self.qty_spin_box.setObjectName(u"qty_spin_box")
        sizePolicy1.setHeightForWidth(self.qty_spin_box.sizePolicy().hasHeightForWidth())
        self.qty_spin_box.setSizePolicy(sizePolicy1)
        self.qty_spin_box.setValue(1)

        self.gridLayout.addWidget(self.qty_spin_box, 3, 3, 1, 2)

        self.name_combo_box = QComboBox(Dialog)
        self.name_combo_box.addItem("")
        self.name_combo_box.addItem("")
        self.name_combo_box.addItem("")
        self.name_combo_box.addItem("")
        self.name_combo_box.setObjectName(u"name_combo_box")
        self.name_combo_box.setMaximumSize(QSize(260, 16777215))
        self.name_combo_box.setEditable(True)

        self.gridLayout.addWidget(self.name_combo_box, 0, 1, 1, 4)


        self.verticalLayout_3.addLayout(self.gridLayout)

        self.line = QFrame(Dialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.sizes_grid = QGridLayout()
        self.sizes_grid.setObjectName(u"sizes_grid")
        self.sizes_table = QTableWidget(Dialog)
        if (self.sizes_table.columnCount() < 3):
            self.sizes_table.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.sizes_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.sizes_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.sizes_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        if (self.sizes_table.rowCount() < 13):
            self.sizes_table.setRowCount(13)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(3, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(4, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(5, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(6, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(7, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(8, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(9, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(10, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(11, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.sizes_table.setVerticalHeaderItem(12, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.sizes_table.setItem(0, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.sizes_table.setItem(1, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.sizes_table.setItem(1, 1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.sizes_table.setItem(2, 0, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.sizes_table.setItem(2, 1, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.sizes_table.setItem(3, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.sizes_table.setItem(3, 1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.sizes_table.setItem(4, 0, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.sizes_table.setItem(4, 1, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.sizes_table.setItem(5, 0, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.sizes_table.setItem(5, 1, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.sizes_table.setItem(6, 0, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.sizes_table.setItem(6, 1, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.sizes_table.setItem(7, 0, __qtablewidgetitem29)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.sizes_table.setItem(8, 0, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.sizes_table.setItem(9, 0, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.sizes_table.setItem(10, 0, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.sizes_table.setItem(11, 0, __qtablewidgetitem33)
        self.sizes_table.setObjectName(u"sizes_table")
        self.sizes_table.setEnabled(True)
        self.sizes_table.setMinimumSize(QSize(0, 310))
        font = QFont()
        font.setPointSize(8)
        font.setKerning(True)
        self.sizes_table.setFont(font)
        self.sizes_table.setTabKeyNavigation(True)
        self.sizes_table.setProperty("showDropIndicator", True)
        self.sizes_table.setDefaultDropAction(Qt.IgnoreAction)
        self.sizes_table.setAlternatingRowColors(True)
        self.sizes_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.sizes_table.setShowGrid(True)
        self.sizes_table.setGridStyle(Qt.SolidLine)
        self.sizes_table.setSortingEnabled(False)
        self.sizes_table.setWordWrap(True)
        self.sizes_table.setCornerButtonEnabled(True)
        self.sizes_table.setRowCount(13)
        self.sizes_table.setColumnCount(3)
        self.sizes_table.horizontalHeader().setVisible(True)
        self.sizes_table.horizontalHeader().setMinimumSectionSize(36)
        self.sizes_table.horizontalHeader().setDefaultSectionSize(100)
        self.sizes_table.horizontalHeader().setHighlightSections(True)
        self.sizes_table.verticalHeader().setVisible(False)
        self.sizes_table.verticalHeader().setCascadingSectionResizes(False)
        self.sizes_table.verticalHeader().setDefaultSectionSize(23)

        self.sizes_grid.addWidget(self.sizes_table, 2, 0, 1, 5)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.sizes_grid.addWidget(self.label, 1, 4, 1, 1)

        self.color_combo_box = QComboBox(Dialog)
        self.color_combo_box.addItem("")
        self.color_combo_box.addItem("")
        self.color_combo_box.addItem("")
        self.color_combo_box.setObjectName(u"color_combo_box")
        sizePolicy1.setHeightForWidth(self.color_combo_box.sizePolicy().hasHeightForWidth())
        self.color_combo_box.setSizePolicy(sizePolicy1)
        self.color_combo_box.setMinimumSize(QSize(80, 0))
        self.color_combo_box.setEditable(True)

        self.sizes_grid.addWidget(self.color_combo_box, 1, 1, 1, 1)

        self.width_label = QLabel(Dialog)
        self.width_label.setObjectName(u"width_label")
        sizePolicy2.setHeightForWidth(self.width_label.sizePolicy().hasHeightForWidth())
        self.width_label.setSizePolicy(sizePolicy2)

        self.sizes_grid.addWidget(self.width_label, 1, 2, 1, 1)

        self.width_combo_box = QComboBox(Dialog)
        self.width_combo_box.addItem("")
        self.width_combo_box.addItem("")
        self.width_combo_box.addItem("")
        self.width_combo_box.setObjectName(u"width_combo_box")
        sizePolicy1.setHeightForWidth(self.width_combo_box.sizePolicy().hasHeightForWidth())
        self.width_combo_box.setSizePolicy(sizePolicy1)
        self.width_combo_box.setMinimumSize(QSize(80, 0))
        self.width_combo_box.setMaximumSize(QSize(16777215, 16777215))
        self.width_combo_box.setEditable(False)

        self.sizes_grid.addWidget(self.width_combo_box, 1, 3, 1, 1)

        self.color_label = QLabel(Dialog)
        self.color_label.setObjectName(u"color_label")
        sizePolicy2.setHeightForWidth(self.color_label.sizePolicy().hasHeightForWidth())
        self.color_label.setSizePolicy(sizePolicy2)

        self.sizes_grid.addWidget(self.color_label, 1, 0, 1, 1)


        self.verticalLayout_3.addLayout(self.sizes_grid)

        self.button_save = QPushButton(Dialog)
        self.button_save.setObjectName(u"button_save")
        sizePolicy1.setHeightForWidth(self.button_save.sizePolicy().hasHeightForWidth())
        self.button_save.setSizePolicy(sizePolicy1)
        self.button_save.setLayoutDirection(Qt.RightToLeft)
        self.button_save.setAutoFillBackground(False)
        self.button_save.setFlat(False)

        self.verticalLayout_3.addWidget(self.button_save)

        self.verticalSpacer = QSpacerItem(514, 163, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        QWidget.setTabOrder(self.name_combo_box, self.buy_price_line_edit)
        QWidget.setTabOrder(self.buy_price_line_edit, self.price_line_edit)
        QWidget.setTabOrder(self.price_line_edit, self.type_combo_box)
        QWidget.setTabOrder(self.type_combo_box, self.qty_spin_box)
        QWidget.setTabOrder(self.qty_spin_box, self.color_combo_box)
        QWidget.setTabOrder(self.color_combo_box, self.width_combo_box)
        QWidget.setTabOrder(self.width_combo_box, self.sizes_table)

        self.retranslateUi(Dialog)

        self.width_combo_box.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
#if QT_CONFIG(tooltip)
        self.qty_label.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.qty_label.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.qty_label.setText(QCoreApplication.translate("Dialog", u"\u041a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e", None))
        self.type_combo_box.setItemText(0, QCoreApplication.translate("Dialog", u"product", None))
        self.type_combo_box.setItemText(1, QCoreApplication.translate("Dialog", u"shoes", None))

        self.type_label.setText(QCoreApplication.translate("Dialog", u"\u0422\u0438\u043f", None))
#if QT_CONFIG(tooltip)
        self.price_label.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.price_label.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.price_label.setText(QCoreApplication.translate("Dialog", u"\u0426\u0435\u043d\u0430 \u043f\u0440\u043e\u0434\u0430\u0436\u0438", None))
        self.name_label.setText(QCoreApplication.translate("Dialog", u"\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435", None))
#if QT_CONFIG(tooltip)
        self.buy_price_label.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.buy_price_label.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.buy_price_label.setText(QCoreApplication.translate("Dialog", u"\u0426\u0435\u043d\u0430 \u043f\u043e\u043a\u0443\u043f\u043a\u0438", None))
        self.name_combo_box.setItemText(0, "")
        self.name_combo_box.setItemText(1, QCoreApplication.translate("Dialog", u"converse chak 70", None))
        self.name_combo_box.setItemText(2, QCoreApplication.translate("Dialog", u"coca cola ", None))
        self.name_combo_box.setItemText(3, QCoreApplication.translate("Dialog", u"nike 70", None))

        ___qtablewidgetitem = self.sizes_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"\u0440\u0430\u0437\u043c\u0435\u0440", None));
        ___qtablewidgetitem1 = self.sizes_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"\u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e", None));
        ___qtablewidgetitem2 = self.sizes_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"\u0434\u0438\u043d\u0430 \u0441\u0442\u0435\u043b\u044c\u043a\u0438", None));

        __sortingEnabled = self.sizes_table.isSortingEnabled()
        self.sizes_table.setSortingEnabled(False)
        ___qtablewidgetitem3 = self.sizes_table.item(0, 0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"35", None));
        ___qtablewidgetitem4 = self.sizes_table.item(1, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("Dialog", u"36", None));
        ___qtablewidgetitem5 = self.sizes_table.item(2, 0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("Dialog", u"37", None));
        ___qtablewidgetitem6 = self.sizes_table.item(3, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("Dialog", u"38", None));
        ___qtablewidgetitem7 = self.sizes_table.item(4, 0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("Dialog", u"39", None));
        ___qtablewidgetitem8 = self.sizes_table.item(5, 0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("Dialog", u"40", None));
        ___qtablewidgetitem9 = self.sizes_table.item(6, 0)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("Dialog", u"41", None));
        ___qtablewidgetitem10 = self.sizes_table.item(7, 0)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("Dialog", u"42", None));
        ___qtablewidgetitem11 = self.sizes_table.item(8, 0)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("Dialog", u"43", None));
        ___qtablewidgetitem12 = self.sizes_table.item(9, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("Dialog", u"44", None));
        ___qtablewidgetitem13 = self.sizes_table.item(10, 0)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("Dialog", u"45", None));
        ___qtablewidgetitem14 = self.sizes_table.item(11, 0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("Dialog", u"46", None));
        self.sizes_table.setSortingEnabled(__sortingEnabled)

        self.label.setText("")
        self.color_combo_box.setItemText(0, "")
        self.color_combo_box.setItemText(1, QCoreApplication.translate("Dialog", u"red", None))
        self.color_combo_box.setItemText(2, QCoreApplication.translate("Dialog", u"black", None))

        self.width_label.setText(QCoreApplication.translate("Dialog", u"\u0448\u0438\u0440\u0438\u043d\u0430", None))
        self.width_combo_box.setItemText(0, QCoreApplication.translate("Dialog", u"D", None))
        self.width_combo_box.setItemText(1, QCoreApplication.translate("Dialog", u"2E", None))
        self.width_combo_box.setItemText(2, QCoreApplication.translate("Dialog", u"4E", None))

        self.color_label.setText(QCoreApplication.translate("Dialog", u"\u0446\u0432\u0435\u0442", None))
        self.button_save.setText(QCoreApplication.translate("Dialog", u"save", None))
    # retranslateUi

