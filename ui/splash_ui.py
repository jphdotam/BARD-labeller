from ui.splash_layout import Ui_MainWindow
from ui.label_ui import LabelUI
from ui.export_ui import ExportUI
from PyQt5 import QtCore
import sys, traceback

if QtCore.QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')
sys.excepthook = excepthook

class MainWindowUI(Ui_MainWindow):
    def __init__(self, mainwindow):
        super(MainWindowUI, self).__init__()
        self.mainwindow = mainwindow
        self.setupUi(mainwindow)
        self.pushButton_ReportCases.clicked.connect(self.run_reportcases_ui)
        self.pushButton_ExportData.clicked.connect(self.run_exportcases_ui)

    def run_reportcases_ui(self):
        print("Running Labeller")
        report_window = LabelUI(self.mainwindow)

    def run_exportcases_ui(self):
        print("Running Exporter")
        export_window = ExportUI(self.mainwindow)