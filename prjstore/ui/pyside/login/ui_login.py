# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginFnEKYX.ui'
##
## Created by: Qt User Interface Compiler version 6.2.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout)

class Ui_Frame(object):
    def setupUi(self, Frame):
        if not Frame.objectName():
            Frame.setObjectName(u"Frame")
        Frame.resize(290, 170)
        Frame.setMaximumSize(QSize(111111, 111111))
        self.horizontalLayout_2 = QHBoxLayout(Frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.frame = QFrame(Frame)
        self.frame.setObjectName(u"frame")
        self.frame.setMaximumSize(QSize(275, 16777215))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.name = QLineEdit(self.frame)
        self.name.setObjectName(u"name")
        self.name.setMinimumSize(QSize(250, 36))
        self.name.setMaximumSize(QSize(111111, 36))
        self.name.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(68, 71, 90);\n"
"	padding: 2px;\n"
"	border: 2px solid #c3ccdf;\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 10px\n"
"}")

        self.verticalLayout.addWidget(self.name)

        self.passw = QLineEdit(self.frame)
        self.passw.setObjectName(u"passw")
        self.passw.setMinimumSize(QSize(0, 36))
        self.passw.setMaximumSize(QSize(1111111, 36))
        self.passw.setStyleSheet(u"QLineEdit {\n"
"	background-color: rgb(68, 71, 90);\n"
"	padding: 2px;\n"
"	border: 2px solid #c3ccdf;\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 10px\n"
"}")
        self.passw.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        self.verticalLayout.addWidget(self.passw)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.ok = QPushButton(self.frame)
        self.ok.setObjectName(u"ok")
        self.ok.setMinimumSize(QSize(120, 36))
        self.ok.setMaximumSize(QSize(16777215, 36))
        self.ok.setStyleSheet(u"QPushButton {\n"
"	background-color:rgb(67, 133, 200);\n"
"	border: 2px solid #c3ccdf;\n"
"	color: rgb(255, 255, 255);\n"
"	border-radius: 10px\n"
"}\n"
"QPushButton:hover {\n"
"	background-color:rgb(85, 170, 255)\n"
"}\n"
"QPushButton:pressed {\n"
"	background-color:rgb(0, 170, 127)\n"
"}")

        self.horizontalLayout.addWidget(self.ok)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addWidget(self.frame)


        self.retranslateUi(Frame)

        QMetaObject.connectSlotsByName(Frame)
    # setupUi

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QCoreApplication.translate("Frame", u"Frame", None))
        self.name.setPlaceholderText(QCoreApplication.translate("Frame", u"Enter your name", None))
        self.passw.setPlaceholderText(QCoreApplication.translate("Frame", u"Enter your pass", None))
        self.ok.setText(QCoreApplication.translate("Frame", u"Ok", None))
    # retranslateUi

