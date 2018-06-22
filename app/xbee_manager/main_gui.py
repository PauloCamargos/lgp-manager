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
        self.search_progress_bar.setValue(0)

        # Instantiating database module
        self.db = database.Banco(database='logah', schema='assets', user='postgres',
        password='admin', port=5432, host='localhost')
        self.db.connection()

        # Connection functions to menu items
        self.menu_version.triggered.connect(self.open_version)
        self.menu_add_equipment.triggered.connect(self.open_associate_equipment)
        self.menu_list_equipment.triggered.connect(self.open_list_equipment)
        self.menu_edit_equipment.triggered.connect(self.open_edit_equipment)

        # Setting up children windows
        # About window
        self.about_window = QtWidgets.QWidget()
        self.about = about.Ui_About()

        # associate_equipment window
        self.associate_equipment_window = QtWidgets.QMainWindow()
        self.associate_equipment = associate_equipment.Ui_AssociateEquipment()
        self.associate_equipment.setupUi(self.associate_equipment_window)
        self.associate_equipment.btn_associate_equipment.clicked.connect(self.associate_equipment_db)
        self.associate_equipment.cbx_xbees.currentIndexChanged.connect(self.fill_xbee_info)

        # List equipment window
        self.list_equipment_window = QtWidgets.QWidget()
        self.list_equipment = list_equipment.Ui_ListEquipment()
        self.list_equipment.setupUi(self.list_equipment_window)
        self.list_equipment.bnt_list_equipment.clicked.connect(self.search_all_equipments_db)

        # Add equipment window
        self.edit_equipment_window = QtWidgets.QMainWindow()
        self.edit_equipment = edit_equipment.Ui_EditEquipment()
        self.edit_equipment.setupUi(self.edit_equipment_window)
        self.edit_equipment.btn_search_equipment.clicked.connect(self.search_equipment_db)
        self.edit_equipment.btn_remove_equipment.clicked.connect(self.remove_equipment_db)
        self.edit_equipment.btn_update_data.clicked.connect(self.update_equipment_db)

        # Getting sectors from database
        self.sector = self.db.selectAllDataFrom(table='sectors')
        # Getting xbees from database
        self.xbees = self.db.selectAllDataFrom(table='xbees')
        # Getting all equipment from database
        self.equipments = self.db.selectAllDataFrom(table='equipments')

        # Populating QComboBox sectors
        for s in sorted(self.sector, key=lambda s:s[1]): # sorting the list
            self.cbx_sectors.addItem(s[1])
        # Populating QComboBox equipments
        for e in sorted(self.equipments, key=lambda e:e[1]): # sorting the list
            self.cbx_equipments.addItem(e[1])

    def update_ui(self):
        # MAIN WINDOW
        self.cbx_sectors.clear()
        self.cbx_equipments.clear()
        # Getting sectors from database
        self.sector = self.db.selectAllDataFrom(table='sectors')
        # Getting xbees from database
        self.xbees = self.db.selectAllDataFrom(table='xbees')
        # Getting all equipment from database
        self.equipments = self.db.selectAllDataFrom(table='equipments')

        # Populating QComboBox sectors
        for s in sorted(self.sector, key=lambda s:s[1]): # sorting the list
            self.cbx_sectors.addItem(s[1])
        # Populating QComboBox equipments
        for e in sorted(self.equipments, key=lambda e:e[1]): # sorting the list
            self.cbx_equipments.addItem(e[1])

        # ASSOCIATE EQUIPMENT WINDOW
        # Clearing old infos
        self.associate_equipment.cbx_xbees.clear()
        self.associate_equipment.list_xbees.clear()
        self.associate_equipment.ledit_description.clear()
        self.associate_equipment.ledit_nserie.clear()
        self.associate_equipment.ledit_function.clear()
        self.associate_equipment.ledit_primary_place.clear()
        self.associate_equipment.statusbar.clearMessage()

        # list equipment window
        # Clearing old infos
        self.list_equipment.list_registered_equipment.clear()

        # Add equipment window
        # Clearing infos
        self.edit_equipment.cbx_equipments.clear()
        self.edit_equipment.ledit_description.clear()
        self.edit_equipment.ledit_nserie.clear()
        self.edit_equipment.ledit_function.clear()
        self.edit_equipment.ledit_primary_place.clear()
        self.edit_equipment.statusbar.clearMessage()

    def show_hello_world(self):
        # start = time.time()
        # self.completed = 0
        # while self.completed < 100.0:
        #     self.completed += 0.0001
        # #     self.completed = 5.0 / time.time() * 100
        #     self.progress_bar.setValue(self.completed)
        print("HELLO WORLD!")

    def open_version(self):
        # About window
        self.about.setupUi(self.about_window)
        self.about_window.show()


    def open_associate_equipment(self, status=''):
        # Add equipment window
        unassociated_xbees = self.db.select_free_xbees()
        print(unassociated_xbees)

        # # Clearing old infos
        self.update_ui()

        self.associate_equipment_window.show()

        # Populating xbees QComboBox and sorting it alphab.
        for x in sorted(unassociated_xbees, key=lambda x:x[2]):
            # print(x) # DEBUG
            if x[3] != 'C' and x[3] != 'R': # if the xbee is an end device
                self.associate_equipment.cbx_xbees.addItem(x[2])

        # Status bar message
        if status == 'added':
            self.associate_equipment.statusbar.show()
            self.associate_equipment.statusbar.showMessage('STATUS: Equipamento associado com sucesso!')
        elif status == 'not added':
            self.associate_equipment.statusbar.show()
            self.associate_equipment.statusbar.showMessage('STATUS: Erro. Preencha as informações corretamente!')


    def open_list_equipment(self):
        # list equipment window

        # Clearing old infos
        self.update_ui()
        self.list_equipment_window.show()


    def open_edit_equipment(self, status=''):
        # Add equipment window

        # Clearing infos
        self.update_ui()

        all_equipments = self.search_all_equipments_db()
        for e in sorted(all_equipments, key=lambda e:e[1]):
                self.edit_equipment.cbx_equipments.addItem(f'{e[1]}')
        self.edit_equipment_window.show()
        if status == 'removed':
            self.edit_equipment.statusbar.show()
            self.edit_equipment.statusbar.showMessage('STATUS: Equipamento removido com sucesso!')
        elif status == 'updated':
            self.edit_equipment.statusbar.show()
            self.edit_equipment.statusbar.showMessage('STATUS: Equipamento atualizado com sucesso!')
        elif status == 'not updated':
            self.edit_equipment.statusbar.show()
            self.edit_equipment.statusbar.showMessage('STATUS: Erro. Preencha as informações corretamente!')


    def associate_equipment_db(self):
        """
         Inserts a record of a equipment and it's associated xbee into
         database.
        """

        option = self.associate_equipment.cbx_xbees.currentText()
        xbee = self.db.selectDataWhere('xbees', 'address_64_bit',option, 'id','address_64_bit')

        description_text = self.associate_equipment.ledit_description.text()
        serial_number_text = self.associate_equipment.ledit_nserie.text()
        equipment_function_text = self.associate_equipment.ledit_function.text()
        primary_sector_text = self.associate_equipment.ledit_primary_place.text()

        if description_text != "" and serial_number_text != "" and  equipment_function_text != "" and  primary_sector_text:
            self.db.insertDataInto(table='equipments',
            description=description_text,
            serial_number=serial_number_text,
            equipment_function=equipment_function_text,
            primary_sector=primary_sector_text,
            xbee=xbee[0]
            )
            print("[OK] Added equipment")
            self.open_associate_equipment(status='added')
        else:
            self.open_associate_equipment(status='not added')

    def remove_equipment_db(self):
        """
        Removes the equipment from the db
        """

        equipment_serial_number = self.edit_equipment.ledit_nserie.text()
        self.db.deleteDataFrom(table='equipments', condition='serial_number', condition_value=equipment_serial_number )
        print('[OK] Deleted equipment')
        self.open_edit_equipment(status='removed')

    def update_equipment_db(self):
        """
        Updates equipment info's
        """
        equipment_serial_number = self.edit_equipment.ledit_nserie.text()
        equipment = self.db.selectDataWhere('equipments', 'serial_number',equipment_serial_number,'serial_number')
        print(equipment)
        ds = self.edit_equipment.ledit_description.text()
        fn = self.edit_equipment.ledit_function.text()
        ps = self.edit_equipment.ledit_primary_place.text()

        if ds != "" and fn != "" and  ps != "":
            self.db.updateDataFrom(table='equipments', condition='serial_number',
            condition_value=equipment[0], description=ds, equipment_function=fn,
            primaryy_sector=ps)
            self.open_edit_equipment(status='updated')
        else:
            self.open_edit_equipment(status='not updated')

    def fill_xbee_info(self):
        self.associate_equipment.list_xbees.clear()
        option = self.associate_equipment.cbx_xbees.currentText()
        # print(option) # DEBUG
        xbee = self.db.selectDataWhere('xbees', 'address_64_bit',option, 'address_64_bit', 'ni')
        # print(xbee)
        if xbee:
            self.associate_equipment.list_xbees.addItem("64 Bit Addr.: " +  xbee[0])
            self.associate_equipment.list_xbees.addItem("NI.: " +  xbee[1])

    def search_all_equipments_db(self):
        """
         Search all equipment in the DB
        """
        self.list_equipment.list_registered_equipment.clear()
        all_equipments = self.db.selectAllDataFrom(table='equipments')
        eq_number = len(all_equipments)
        i=1
        for a in all_equipments:
            # print(a) # DEBUG
            self.list_equipment.list_registered_equipment.addItem(f"{i}) {a[1]} ({a[4]})")
            i+=1
        return all_equipments

    def search_equipment_db(self):
        """
        Searches one equipment in the DB and update GUI fileds
        """
        option = self.edit_equipment.cbx_equipments.currentText()
        equipment = self.db.selectDataWhere('equipments', 'description',option, 'serial_number', 'equipment_function', 'primary_sector')
        self.edit_equipment.ledit_description.setText(option)
        self.edit_equipment.ledit_nserie.setText(equipment[0])
        self.edit_equipment.ledit_function.setText(equipment[1])
        self.edit_equipment.ledit_primary_place.setText(equipment[2])


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
