#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from views import base

class LogahApp(QMainWindow, base.Ui_MainWindow):
    def __init__(self, parent=None):
        super(LogahApp, self).__init__(parent)
        self.setupUi(self)
        self.btn_devices.clicked.connect(self.show_hello_world)

    def show_hello_world(self):
        self.list_devices.addItem("Hello World!")


def main():
    app = QApplication(sys.argv)
    form = LogahApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
