import sys
from PyQt5 import QtWidgets
from ui.label_ui import LabelUI
from ui.splash_ui import MainWindowUI

def run():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUI(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

run()