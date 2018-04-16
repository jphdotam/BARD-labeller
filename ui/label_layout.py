# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './label.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1680, 1005)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_ECG = QtWidgets.QVBoxLayout()
        self.verticalLayout_ECG.setObjectName("verticalLayout_ECG")
        self.label_FileSelector = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_FileSelector.setFont(font)
        self.label_FileSelector.setObjectName("label_FileSelector")
        self.verticalLayout_ECG.addWidget(self.label_FileSelector)
        self.comboBox_txtFiles = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_txtFiles.setEnabled(False)
        self.comboBox_txtFiles.setObjectName("comboBox_txtFiles")
        self.comboBox_txtFiles.addItem("")
        self.verticalLayout_ECG.addWidget(self.comboBox_txtFiles)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_ECG = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_ECG.setFont(font)
        self.label_ECG.setObjectName("label_ECG")
        self.horizontalLayout_4.addWidget(self.label_ECG)
        self.pushButton_SeparationInc = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_SeparationInc.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/arrow-126-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_SeparationInc.setIcon(icon)
        self.pushButton_SeparationInc.setObjectName("pushButton_SeparationInc")
        self.horizontalLayout_4.addWidget(self.pushButton_SeparationInc)
        self.pushButton_SeparationDec = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_SeparationDec.setEnabled(False)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/arrow-188-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_SeparationDec.setIcon(icon1)
        self.pushButton_SeparationDec.setObjectName("pushButton_SeparationDec")
        self.horizontalLayout_4.addWidget(self.pushButton_SeparationDec)
        self.verticalLayout_ECG.addLayout(self.horizontalLayout_4)
        self.graphicsView_ = PlotWidget(self.centralwidget)
        self.graphicsView_.setObjectName("graphicsView_")
        self.verticalLayout_ECG.addWidget(self.graphicsView_)
        self.gridLayout.addLayout(self.verticalLayout_ECG, 0, 1, 1, 1)
        self.verticalLayout_Labels = QtWidgets.QVBoxLayout()
        self.verticalLayout_Labels.setObjectName("verticalLayout_Labels")
        self.label_Labels = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_Labels.setFont(font)
        self.label_Labels.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_Labels.setObjectName("label_Labels")
        self.verticalLayout_Labels.addWidget(self.label_Labels)
        self.verticalLayout_Ranges = QtWidgets.QVBoxLayout()
        self.verticalLayout_Ranges.setObjectName("verticalLayout_Ranges")
        self.label_Ranges = QtWidgets.QLabel(self.centralwidget)
        self.label_Ranges.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Ranges.setObjectName("label_Ranges")
        self.verticalLayout_Ranges.addWidget(self.label_Ranges)
        self.tableWidget_Ranges = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_Ranges.setObjectName("tableWidget_Ranges")
        self.tableWidget_Ranges.setColumnCount(0)
        self.tableWidget_Ranges.setRowCount(0)
        self.verticalLayout_Ranges.addWidget(self.tableWidget_Ranges)
        self.verticalLayout_Labels.addLayout(self.verticalLayout_Ranges)
        self.verticalLayout_Markers = QtWidgets.QVBoxLayout()
        self.verticalLayout_Markers.setObjectName("verticalLayout_Markers")
        self.label_Markers = QtWidgets.QLabel(self.centralwidget)
        self.label_Markers.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Markers.setObjectName("label_Markers")
        self.verticalLayout_Markers.addWidget(self.label_Markers)
        self.tableWidget_Markers = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_Markers.setObjectName("tableWidget_Markers")
        self.tableWidget_Markers.setColumnCount(0)
        self.tableWidget_Markers.setRowCount(0)
        self.verticalLayout_Markers.addWidget(self.tableWidget_Markers)
        self.verticalLayout_Labels.addLayout(self.verticalLayout_Markers)
        self.gridLayout.addLayout(self.verticalLayout_Labels, 0, 2, 1, 1)
        self.verticalLayout_Buttons = QtWidgets.QVBoxLayout()
        self.verticalLayout_Buttons.setObjectName("verticalLayout_Buttons")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_PatientData = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.label_PatientData.setFont(font)
        self.label_PatientData.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_PatientData.setObjectName("label_PatientData")
        self.verticalLayout.addWidget(self.label_PatientData)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_PatientID = QtWidgets.QLabel(self.centralwidget)
        self.label_PatientID.setObjectName("label_PatientID")
        self.horizontalLayout_3.addWidget(self.label_PatientID)
        self.lineEdit_PatientID = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_PatientID.setEnabled(False)
        self.lineEdit_PatientID.setObjectName("lineEdit_PatientID")
        self.horizontalLayout_3.addWidget(self.lineEdit_PatientID)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_ProcedureDate = QtWidgets.QLabel(self.centralwidget)
        self.label_ProcedureDate.setObjectName("label_ProcedureDate")
        self.horizontalLayout_2.addWidget(self.label_ProcedureDate)
        self.dateEdit_ProcedureDate = QtWidgets.QDateEdit(self.centralwidget)
        self.dateEdit_ProcedureDate.setEnabled(False)
        self.dateEdit_ProcedureDate.setObjectName("dateEdit_ProcedureDate")
        self.horizontalLayout_2.addWidget(self.dateEdit_ProcedureDate)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_ProcedureType = QtWidgets.QLabel(self.centralwidget)
        self.label_ProcedureType.setObjectName("label_ProcedureType")
        self.horizontalLayout.addWidget(self.label_ProcedureType)
        self.comboBox_ProcedureType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_ProcedureType.setEnabled(False)
        self.comboBox_ProcedureType.setObjectName("comboBox_ProcedureType")
        self.horizontalLayout.addWidget(self.comboBox_ProcedureType)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_ProtocolButtons = QtWidgets.QVBoxLayout()
        self.verticalLayout_ProtocolButtons.setObjectName("verticalLayout_ProtocolButtons")
        self.verticalLayout_3.addLayout(self.verticalLayout_ProtocolButtons)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_Buttons.addLayout(self.verticalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout_Buttons, 0, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 4)
        self.gridLayout.setColumnStretch(2, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1680, 22))
        self.menubar.setObjectName("menubar")
        self.menuHello = QtWidgets.QMenu(self.menubar)
        self.menuHello.setObjectName("menuHello")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setEnabled(True)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionLoad_patient = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/Patient.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_patient.setIcon(icon2)
        self.actionLoad_patient.setObjectName("actionLoad_patient")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/About.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon3)
        self.actionAbout.setObjectName("actionAbout")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuHello.addAction(self.actionLoad_patient)
        self.menuHello.addSeparator()
        self.menuHello.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHello.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actionLoad_patient)
        self.toolBar.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        self.comboBox_ProcedureType.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        qtRectangle = MainWindow.frameGeometry()
        centerPoint = QtWidgets.QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        MainWindow.move(qtRectangle.topLeft())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BARD labeller"))
        self.label_FileSelector.setText(_translate("MainWindow", "File selector"))
        self.comboBox_txtFiles.setCurrentText(_translate("MainWindow", "Please select a file"))
        self.comboBox_txtFiles.setItemText(0, _translate("MainWindow", "Please select a file"))
        self.label_ECG.setText(_translate("MainWindow", "ECG"))
        self.pushButton_SeparationInc.setText(_translate("MainWindow", "Separation"))
        self.pushButton_SeparationDec.setText(_translate("MainWindow", "Separation"))
        self.label_Labels.setText(_translate("MainWindow", "Labels"))
        self.label_Ranges.setText(_translate("MainWindow", "Ranges"))
        self.label_Markers.setText(_translate("MainWindow", "Markers"))
        self.label_PatientData.setText(_translate("MainWindow", "Patient Data"))
        self.label_PatientID.setText(_translate("MainWindow", "Patient ID"))
        self.label_ProcedureDate.setText(_translate("MainWindow", "Procedure Date"))
        self.label_ProcedureType.setText(_translate("MainWindow", "Procedure Type"))
        self.menuHello.setTitle(_translate("MainWindow", "File"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionLoad_patient.setText(_translate("MainWindow", "Load patient"))
        self.actionLoad_patient.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

from pyqtgraph import PlotWidget