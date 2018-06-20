#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import time
import threading_tutorial as base

class ThreadApp(QMainWindow, base.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ThreadApp, self).__init__(parent)
        self.setupUi(self)
    #     self.progress_bar.setValue(0)
    #
    #     # Connection functions to buttons
    #     self.btn_devices.clicked.connect(self.show_hello_world)
    #     self.list_devices.addItem("Oxímetro Portátil Bioland")
    #     self.list_devices.addItem("Ventilador mecânico Siare")
    #     self.list_devices.addItem("Notebook Dell Inpiron 5448")
    #     self.list_devices.addItem("Cadeira de rodas Ortobras 250Kg")
    #
    # def show_hello_world(self):
    #
    #
    #     # start = time.time()
    #     self.completed = 0
    #     while self.completed < 100.0:
    #         self.completed += 0.000001
    #     #     self.completed = 5.0 / time.time() * 100
    #         self.progress_bar.setValue(self.completed)



def main():
    app = QApplication(sys.argv)
    form = ThreadApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    main()
