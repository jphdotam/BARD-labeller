from PyQt5 import QtCore
import traceback
import sys
from ui.export_layout import Ui_MainWindow

if QtCore.QT_VERSION >= 0x50501:
    def excepthook(type_, value, traceback_):
        traceback.print_exception(type_, value, traceback_)
        QtCore.qFatal('')
sys.excepthook = excepthook

class ExportUI(Ui_MainWindow):
    def __init__(self, mainwindow):
        super(ExportUI, self).__init__()
        self.setupUi(mainwindow)