#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import time
from views import base
from controller import xbee_handler

class LogahApp(QMainWindow, base.Ui_MainWindow):
    def __init__(self, parent=None):
        super(LogahApp, self).__init__(parent)
        self.setupUi(self)
        self.progress_bar.setValue(0)

        # Connection functions to buttons
        self.btn_devices.clicked.connect(self.show_hello_world)

    def show_hello_world(self):
        self.list_devices.addItem("Hello World!")
        start = time.time()
        self.completed = 0
        while self.completed < 100.0:
            # self.completed += 0.00005
            self.completed = 5.0 / time.time() * 100
            self.progress_bar.setValue(self.completed)



def main():
    app = QApplication(sys.argv)
    form = LogahApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    xbee = xbee_handler.XBeeHandler()
    try:
        xbee.openCoordinatorCom()
        main()
    finally:
        xbee.closeCoordinatorCom()
