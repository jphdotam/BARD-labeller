# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './splash.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.pushButton_ReportCases = QtWidgets.QPushButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/label_ecg.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_ReportCases.setIcon(icon)
        self.pushButton_ReportCases.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_ReportCases.setObjectName("pushButton_ReportCases")
        self.verticalLayout.addWidget(self.pushButton_ReportCases)
        self.pushButton_ExportData = QtWidgets.QPushButton(self.centralwidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/export_data.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_ExportData.setIcon(icon1)
        self.pushButton_ExportData.setIconSize(QtCore.QSize(100, 100))
        self.pushButton_ExportData.setObjectName("pushButton_ExportData")
        self.verticalLayout.addWidget(self.pushButton_ExportData)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">BARD Labeller</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Copyright Dr James P Howard 2018</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Wellcome Trust Clinical Research Fellow</span></p><p><br/></p></body></html>"))
        self.pushButton_ReportCases.setText(_translate("MainWindow", "Report Cases"))
        self.pushButton_ExportData.setText(_translate("MainWindow", "Export Data"))

