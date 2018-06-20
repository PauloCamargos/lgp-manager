#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread
import sys
import time
from views import main_window, about, add_equipment
from controller import xbee_handler
from controller import database

class LogahApp(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(LogahApp, self).__init__(parent)
        self.setupUi(self)
        self.progress_bar.setValue(0)

        # Instantiating database module
        db = database.Banco(database='logah', schema='assets', user='postgres',
        password='postgres', port=5432, host='localhost')

        # # Connection functions to buttons
        # self.btn_devices.clicked.connect(self.show_hello_world)
        # self.list_devices.addItem("Oxímetro Portátil Bioland")
        # self.list_devices.addItem("Ventilador mecânico Siare")
        # self.list_devices.addItem("Notebook Dell Inpiron 5448")
        # self.list_devices.addItem("Cadeira de rodas Ortobras 250Kg")

    def show_hello_world(self):
        # start = time.time()
        self.completed = 0
        while self.completed < 100.0:
            self.completed += 0.0001
        #     self.completed = 5.0 / time.time() * 100
            self.progress_bar.setValue(self.completed)


class DiscoveryThread(QThread):
    def __init__(self, device_name):
        QThread.__init__(self)
        self.device_name = device_name

    def __del__(self):
        self.wait()

    def getDevices(self):
        devices = xbee.getSectorEquipments(self.device_name)


def main():
    app = QApplication(sys.argv)
    form = LogahApp()
    form.show()
    app.exec_()


if __name__ == "__main__":
    xbee = xbee_handler.XBeeHandler()
    try:
        if xbee.coordinator is not None:
            xbee.openCoordinatorCom()
        main()
    finally:
        if xbee.coordinator is not None:
            xbee.closeCoordinatorCom()
