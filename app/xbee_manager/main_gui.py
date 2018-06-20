#!/usr/bin/python3
# -*- coding: utf-8 -*

from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread
import sys
import time
from views import main_window, about, associate_equipment, list_equipment, edit_equipment
from controller import xbee_handler
from controller import database


class LogahApp(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, parent=None):
        super(LogahApp, self).__init__(parent)
        self.setupUi(self)
        self.progress_bar.setValue(0)

        # Instantiating database module
        self.db = database.Banco(database='logah', schema='assets', user='postgres',
        password='admin', port=5432, host='localhost')
        self.db.connection()

        # # Connection functions to buttons
        # self.btn_devices.clicked.connect(self.show_hello_world)
        # self.list_devices.addItem("Oxímetro Portátil Bioland")
        # self.list_devices.addItem("Ventilador mecânico Siare")
        # self.list_devices.addItem("Notebook Dell Inpiron 5448")
        # self.list_devices.addItem("Cadeira de rodas Ortobras 250Kg")
        self.menu_version.triggered.connect(self.open_version)
        self.menu_add_equipment.triggered.connect(self.open_associate_equipment)
        self.menu_list_equipment.triggered.connect(self.open_list_equipment)
        self.menu_edit_equipment.triggered.connect(self.open_edit_equipment)



    def show_hello_world(self):
        # start = time.time()
        self.completed = 0
        while self.completed < 100.0:
            self.completed += 0.0001
        #     self.completed = 5.0 / time.time() * 100
            self.progress_bar.setValue(self.completed)


    def open_version(self):
        # About window
        self.about_window = QtWidgets.QWidget()
        self.about = about.Ui_About()
        self.about.setupUi(self.about_window)
        self.about_window.show()


    def open_associate_equipment(self):
        # Add equipment window
        self.associate_equipment_window = QtWidgets.QMainWindow()
        self.associate_equipment = associate_equipment.Ui_AssociateEquipment()
        self.associate_equipment.setupUi(self.associate_equipment_window)
        self.associate_equipment.btn_associate_equipment.clicked.connect(self.associate_equipment_db)
        self.associate_equipment_window.show()


    def open_list_equipment(self):
        # Add equipment window
        self.list_equipment_window = QtWidgets.QWidget()
        self.list_equipment = list_equipment.Ui_ListEquipment()
        self.list_equipment.setupUi(self.list_equipment_window)
        self.list_equipment_window.show()


    def open_edit_equipment(self):
        # Add equipment window
        self.edit_equipment_window = QtWidgets.QWidget()
        self.edit_equipment = edit_equipment.Ui_EditEquipment()
        self.edit_equipment.setupUi(self.edit_equipment_window)
        self.edit_equipment_window.show()


    def associate_equipment_db(self):
        # db.insertDataInto()
        print(self.associate_equipment.ledit_descritpion.text())
        self.db.insertDataInto(table='equipments',
        description=self.associate_equipment.ledit_descritpion.text(),
        serial_number=self.associate_equipment.ledit_nserie.text(),
        equipment_function=self.associate_equipment.ledit_function.text(),
        primarary_sector=self.associate_equipment.ledit_primary_place.text()
        )
        print("[OK] Added equipment")
        self.associate_equipment.statusbar.show()
        self.associate_equipment.statusbar.showMessage('Equipamento associado com sucesso!')


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
