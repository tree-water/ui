# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'UI_show.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(556, 500)
        self.verticalLayout_5 = QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 100))
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout_4.addWidget(self.label)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.pushButton_start = QPushButton(Form)
        self.pushButton_start.setObjectName(u"pushButton_start")
        self.pushButton_start.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.pushButton_start)

        self.pushButton_stop = QPushButton(Form)
        self.pushButton_stop.setObjectName(u"pushButton_stop")
        self.pushButton_stop.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.pushButton_stop)

        self.pushButton_show = QPushButton(Form)
        self.pushButton_show.setObjectName(u"pushButton_show")
        self.pushButton_show.setMinimumSize(QSize(150, 0))
        self.pushButton_show.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.pushButton_show)

        self.pushButton_rssi = QPushButton(Form)
        self.pushButton_rssi.setObjectName(u"pushButton_rssi")
        self.pushButton_rssi.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.pushButton_rssi)

        self.pushButton_hiderssi = QPushButton(Form)
        self.pushButton_hiderssi.setObjectName(u"pushButton_hiderssi")
        self.pushButton_hiderssi.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.pushButton_hiderssi)

        self.pushButton_phase = QPushButton(Form)
        self.pushButton_phase.setObjectName(u"pushButton_phase")
        self.pushButton_phase.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.pushButton_phase)

        self.pushButton_hidephase = QPushButton(Form)
        self.pushButton_hidephase.setObjectName(u"pushButton_hidephase")
        self.pushButton_hidephase.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout.addWidget(self.pushButton_hidephase)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)


        self.verticalLayout_5.addLayout(self.verticalLayout_4)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u8bfb\u53d6\u6570\u636e\u5c55\u793a", None))
        self.pushButton_start.setText(QCoreApplication.translate("Form", u"\u5f00\u59cb\u8bfb\u53d6", None))
        self.pushButton_stop.setText(QCoreApplication.translate("Form", u"\u505c\u6b62\u8bfb\u53d6", None))
        self.pushButton_show.setText(QCoreApplication.translate("Form", u"\u5c55\u73b0\u6807\u7b7eID", None))
        self.pushButton_rssi.setText(QCoreApplication.translate("Form", u"\u5e45\u5ea6\u56fe", None))
        self.pushButton_hiderssi.setText(QCoreApplication.translate("Form", u"\u9690\u85cf\u5e45\u5ea6\u56fe", None))
        self.pushButton_phase.setText(QCoreApplication.translate("Form", u"\u76f8\u4f4d\u56fe", None))
        self.pushButton_hidephase.setText(QCoreApplication.translate("Form", u"\u9690\u85cf\u76f8\u4f4d\u56fe", None))
    # retranslateUi

