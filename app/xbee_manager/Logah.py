#!/usr/bin/python3
# -*- coding: utf-8 -*

# PyQt5 threading example https://kushaldas.in/posts/pyqt5-thread-example.html
from digi.xbee.exception import TimeoutException, InvalidOperatingModeException

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from views import main_window, about, associate_equipment, list_equipment, \
                    edit_equipment
from controller import xbee_handler
from controller import database
import sys
import time

class LgpApp(QMainWindow, main_window.Ui_MainWindow):
    signal_start_search = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(LgpApp, self).__init__(parent)
        self.setupUi(self)

        self.search_progress_bar.setValue(0)
        self.search_progress_bar.setMaximum(5)

        # Instantiating database module
        self.db = database.Banco(database='lgp', schema='assets',\
        user='postgres',
        password='admin', port=5432, host='localhost')
        self.db.connection()

        # Connecting buttons to functions
        self.btn_search_devices.clicked.connect(self.search_sectors_equipment)
        self.btn_search_sector.clicked.connect(self.search_sector_by_equipment)

        # Connecting functions to menu items
        self.menu_version.triggered.connect(self.open_version)
        self.menu_add_equipment.triggered.connect(self.open_associate_equipment)
        self.menu_list_equipment.triggered.connect(self.open_list_equipment)
        self.menu_edit_equipment.triggered.connect(self.open_edit_equipment)

        # Setting up children windows
        # About window
        self.about_window = QtWidgets.QWidget()
        self.about = about.Ui_About()

        # Associate equipment window
        self.associate_equipment_window = QtWidgets.QMainWindow()
        self.associate_equipment = associate_equipment.Ui_AssociateEquipment()
        self.associate_equipment.setupUi(self.associate_equipment_window)
        self.associate_equipment.btn_associate_equipment.clicked.connect(
        self.associate_equipment_db
        )
        self.associate_equipment.cbx_xbees.currentIndexChanged.connect(
        self.fill_xbee_info
        )

        # List equipment window
        self.list_equipment_window = QtWidgets.QWidget()
        self.list_equipment = list_equipment.Ui_ListEquipment()
        self.list_equipment.setupUi(self.list_equipment_window)
        self.list_equipment.bnt_list_equipment.clicked.connect(
        self.search_all_equipments
        )
        self.list_equipment.list_progress_bar.setValue(0)
        self.list_equipment.list_progress_bar.setMaximum(5)

        # Add equipment window
        self.edit_equipment_window = QtWidgets.QMainWindow()
        self.edit_equipment = edit_equipment.Ui_EditEquipment()
        self.edit_equipment.setupUi(self.edit_equipment_window)
        self.edit_equipment.btn_search_equipment.clicked.connect(
        self.search_equipment_db
        )
        self.edit_equipment.btn_remove_equipment.clicked.connect(
        self.remove_equipment_db
        )
        self.edit_equipment.btn_update_data.clicked.connect(
        self.update_equipment_db
        )

        # Getting sectors from database
        self.sector = self.db.selectAllDataFrom(table='sectors')
        # Getting all equipment from database
        self.equipments = self.db.selectAllDataFrom(table='equipments')

        # Populating QComboBox sectors
        for s in sorted(self.sector, key=lambda s:s[1]): # sorting the list
            self.cbx_sectors.addItem(s[1])
        # Populating QComboBox equipments
        for e in sorted(self.equipments, key=lambda e:e[1]): # sorting the list
            self.cbx_equipments.addItem(e[1])

    def coordinator_not_found(self):
        self.msg = QMessageBox()
        self.msg.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Dispositivo de localização não encontrado. Conecte-o "
        "e execute o programa novamente.")
        self.msg.setWindowTitle("Erro")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.buttonClicked.connect(self.close_message_box)
        self.msg.show()

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
        self.list_equipment.list_found_equipment.clear()
        self.list_equipment.list_progress_bar.setValue(0)
        self.list_equipment.list_progress_bar.setMaximum(5)
        # Add equipment window
        # Clearing infos
        self.edit_equipment.cbx_equipments.clear()
        self.edit_equipment.ledit_description.clear()
        self.edit_equipment.ledit_nserie.clear()
        self.edit_equipment.ledit_function.clear()
        self.edit_equipment.ledit_primary_place.clear()
        self.edit_equipment.statusbar.clearMessage()

    def show_hello_world(self):
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
            self.associate_equipment.statusbar.showMessage('STATUS: Equipamento ' \
             'associado com sucesso!')
        elif status == 'not added':
            self.associate_equipment.statusbar.show()
            self.associate_equipment.statusbar.showMessage('STATUS: Erro. ' \
            'Preencha as informações corretamente!')

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
            self.edit_equipment.statusbar.showMessage('STATUS: Equipamento ' \
            'removido com sucesso!')
        elif status == 'updated':
            self.edit_equipment.statusbar.show()
            self.edit_equipment.statusbar.showMessage('STATUS: Equipamento ' \
             'atualizado com sucesso!')
        elif status == 'not updated':
            self.edit_equipment.statusbar.show()
            self.edit_equipment.statusbar.showMessage('STATUS: Erro. Preencha '\
             'as informações corretamente!')

    def associate_equipment_db(self):
        """
         Inserts a record of a equipment and it's associated xbee into
         database.
        """

        option = self.associate_equipment.cbx_xbees.currentText()
        xbee = self.db.selectDataWhere('xbees', 'address_64_bit',option, 'id',
        'address_64_bit')

        description_text = self.associate_equipment.ledit_description.text()
        serial_number_text = self.associate_equipment.ledit_nserie.text()
        equipment_function_text = self.associate_equipment.ledit_function.text()
        primary_sector_text = self.associate_equipment.ledit_primary_place.text()

        if description_text != "" and serial_number_text != "" \
        and  equipment_function_text != "" and  primary_sector_text:
            self.db.insertDataInto(
            table='equipments',
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
        self.db.deleteDataFrom(table='equipments', condition='serial_number',
        condition_value=equipment_serial_number )
        print('[OK] Deleted equipment')
        self.open_edit_equipment(status='removed')

    def update_equipment_db(self):
        """
        Updates equipment info's
        """
        equipment_serial_number = self.edit_equipment.ledit_nserie.text()
        equipment = self.db.selectDataWhere('equipments', 'serial_number',
        equipment_serial_number,'serial_number')
        print(equipment)
        ds = self.edit_equipment.ledit_description.text()
        fn = self.edit_equipment.ledit_function.text()
        ps = self.edit_equipment.ledit_primary_place.text()

        if ds != "" and fn != "" and  ps != "":
            self.db.updateDataFrom(table='equipments',condition='serial_number',
            condition_value=equipment[0], description=ds, equipment_function=fn,
            primary_sector=ps)
            self.open_edit_equipment(status='updated')
        else:
            self.open_edit_equipment(status='not updated')

    def fill_xbee_info(self):
        self.associate_equipment.list_xbees.clear()
        option = self.associate_equipment.cbx_xbees.currentText()
        # print(option) # DEBUG
        xbee = self.db.selectDataWhere('xbees', 'address_64_bit',option, \
        'address_64_bit', 'ni')
        # print(xbee)
        if xbee:
            self.associate_equipment.list_xbees.addItem("64 Bit Addr.: " +  \
            xbee[0])
            self.associate_equipment.list_xbees.addItem("NI.: " +  xbee[1])

    def search_all_equipments(self):
        self.search_all_equipments_db()

        self.list_equipment.search_equipment_thread = DiscoverEquipmentsBySector("All")
        # Connect the signal from the thread to the finished method
        self.list_equipment.search_equipment_thread.signal_status.connect(
        self.list_window_thread_manager
        )
        self.list_equipment.search_equipment_thread.signal_number_of_connected_devices.connect(
        self.configure_list_progress_bar
        )
        self.list_equipment.search_equipment_thread.signal_discovered_device.connect(
        self.list_all_equipments
        )
        self.list_equipment.search_equipment_thread.signal_update_progress_bar.connect(
        self.update_list_progress_bar
        )

        self.list_equipment.bnt_list_equipment.setEnabled(False)
        # self.statusBar.show()
        # self.statusBar.showMessage('Aguarde, buscando equipamentos...')
        self.list_equipment.list_progress_bar.setValue(0)
        self.list_equipment.list_progress_bar.setMaximum(5)
        self.list_equipment.search_equipment_thread.start()

    def search_all_equipments_db(self):
        """
         Search all equipment in the DB
        """
        self.list_equipment.list_registered_equipment.clear()
        self.list_equipment.list_found_equipment.clear()

        all_equipments = self.db.selectAllDataFrom(table='equipments')
        eq_number = len(all_equipments)
        i=1
        for a in all_equipments:
            # print(a) # DEBUG
            self.list_equipment.list_registered_equipment.addItem(f"{i}) " \
            f"{a[1]} ({a[4]})")
            i+=1
        return all_equipments

    def search_equipment_db(self):
        """
        Searches one equipment in the DB and update GUI fileds
        """
        option = self.edit_equipment.cbx_equipments.currentText()
        equipment = self.db.selectDataWhere('equipments', 'description',option,
        'serial_number', 'equipment_function', 'primary_sector')
        self.edit_equipment.ledit_description.setText(option)
        self.edit_equipment.ledit_nserie.setText(equipment[0])
        self.edit_equipment.ledit_function.setText(equipment[1])
        self.edit_equipment.ledit_primary_place.setText(equipment[2])

    def search_sectors_equipment(self):
        """
            Searches all equipment inside a sector
        """
        self.list_devices.clear()

        option = self.cbx_sectors.currentText()

        # Creating a thread
        self.search_equipment_thread = DiscoverEquipmentsBySector(option)
        # Connect the signal from the thread to the finished method
        self.search_equipment_thread.signal_status.connect(
        self.main_window_thread_manager
        )
        self.search_equipment_thread.signal_number_of_connected_devices.connect(
        self.configure_progress_bar
        )
        self.search_equipment_thread.signal_discovered_device.connect(
        self.list_discovered_equipments
        )
        self.search_equipment_thread.signal_update_progress_bar.connect(
        self.update_progress_bar
        )

        self.btn_search_devices.setEnabled(False)
        self.btn_search_sector.setEnabled(False)
        self.statusBar.show()
        self.statusBar.showMessage('Aguarde, buscando equipamentos...')
        self.search_progress_bar.setValue(0)
        self.search_progress_bar.setMaximum(5)
        self.search_equipment_thread.start()

    def configure_list_progress_bar(self, maximum):
        self.list_equipment.list_progress_bar.setValue(0)
        self.list_equipment.list_progress_bar.setMaximum(maximum+1)

    def configure_progress_bar(self, maximum):
        self.search_progress_bar.setValue(0)
        self.search_progress_bar.setMaximum(maximum+1)

    def update_progress_bar(self, signal_status):
        if signal_status == 'loading':
            # update progress bar
            self.search_progress_bar.setValue(
            self.search_progress_bar.value()+1
            )

    def update_list_progress_bar(self, signal_status):
        if signal_status == 'loading':
            # update progress bar
            self.list_equipment.list_progress_bar.setValue(
            self.list_equipment.list_progress_bar.value()+1
            )

    def main_window_thread_manager(self, signal_status):
        if signal_status == 'finnished':
            if self.search_progress_bar.value() < \
            self.search_progress_bar.maximum():
                # Completing progress bar case it's not been completed
                self.search_progress_bar.setValue(
                self.search_progress_bar.maximum()
                )

            self.statusBar.show()
            self.statusBar.showMessage('Busca finalizada.')
        elif signal_status == 'busy':
            self.msg = QMessageBox()
            self.msg.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Aguarde um instante. As informações estão sendo " \
            "atualizadas.")
            self.msg.setInformativeText("Um equipamento foi inserido ou removido. " \
            "A rede está sendo reconfigurada.")
            self.msg.setWindowTitle("Aguarde")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.close_message_box)
            self.msg.show()
            self.statusBar.show()
            self.statusBar.showMessage('Busca finalizada.')

        self.btn_search_devices.setEnabled(True)
        self.btn_search_sector.setEnabled(True)

    def close_message_box(self):
        self.msg.close()

    def list_window_thread_manager(self, signal_status):
        if signal_status == 'finnished':
            if self.list_equipment.list_progress_bar.value() < \
            self.list_equipment.list_progress_bar.maximum():
                # Completing progress bar case it's not been completed
                self.list_equipment.list_progress_bar.setValue(
                self.list_equipment.list_progress_bar.maximum()
                )
        elif signal_status == 'busy':
            self.msg = QMessageBox()
            self.msg.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Aguarde um instante. As informações estão sendo " \
            "atualizadas.")
            self.msg.setInformativeText("Um equipamento foi inserido ou removido. " \
            "A rede está sendo reconfigurada.")
            self.msg.setWindowTitle("Aguarde")
            self.msg.setStandardButtons(QMessageBox.Ok)
            self.msg.buttonClicked.connect(self.close_message_box)
            self.msg.show()
            self.statusBar.show()
            self.statusBar.showMessage('Busca finalizada.')

        self.list_equipment.bnt_list_equipment.setEnabled(True)

    def list_discovered_equipments(self, discovered_device=""):
        """
            Lists all register equipement inside a sector
        """
        # if a device was discovered
        if discovered_device != "":
            # If a device was discorever
            print("[INFO] Searching for xbee description in database...")
            device_description = self.db.select_equipment_by_xbee(discovered_device)
            self.list_devices.addItem(device_description[0])
        else:
            # show message 'not found'
            self.list_devices.addItem("Nenhum dispositivo encontrado neste " \
            "setor")

    def list_all_equipments(self, discovered_device):
        if discovered_device != "":
            # If a device was discorever
            print("Searching for xbee description in database")
            device_description = self.db.select_equipment_by_xbee(discovered_device)
            self.list_equipment.list_found_equipment.addItem(device_description[0])
        else:
            # show message 'not found'
            self.list_equipment.list_found_equipment.addItem("Nenhum " \
            "dispositivo encontrado.")

    def search_sector_by_equipment(self):
        self.list_sector.clear()
        option = self.cbx_equipments.currentText()

        equipment_ni = self.db.select_equipment_ni(option)

        # Creating a thread
        self.search_equipment_thread = SearchSectorByEquipment(equipment_ni[0])
        # Connect the signal from the thread to the finished method
        self.search_equipment_thread.signal_status.connect(
        self.main_window_thread_manager
        )
        self.search_equipment_thread.signal_number_of_connected_devices.connect(
        self.configure_progress_bar
        )
        self.search_equipment_thread.signal_update_progress_bar.connect(
        self.update_progress_bar
        )
        self.search_equipment_thread.signal_discovered_device.connect(
        self.list_discovered_sector
        )

        self.btn_search_devices.setEnabled(False)
        self.btn_search_sector.setEnabled(False)
        self.statusBar.show()
        self.statusBar.showMessage('Aguarde, buscando...')
        self.search_progress_bar.setValue(0)
        self.search_progress_bar.setMaximum(5)
        self.search_equipment_thread.start()

    def list_discovered_sector(self, sector_xbee_64_bit_address):
        self.list_equipment.list_found_equipment.clear()
        if sector_xbee_64_bit_address != "":
            # If a device was discorever
            sector_description = self.db.select_sector_description(
            sector_xbee_64_bit_address
            )
            self.list_sector.addItem(sector_description[0])
        else:
            # show message 'not found'
            self.list_sector.addItem("Equipamento não encontrado")


class SearchSectorByEquipment(QThread):
    """
        Class used as a thread to search all sectors in an ambient and check
        if an equipment is present inside this ambient
    """
    signal_status = pyqtSignal(str)
    signal_number_of_connected_devices = pyqtSignal(int)
    signal_discovered_device = pyqtSignal(str)
    signal_update_progress_bar = pyqtSignal(str)

    def __init__(self, equipment_ni=""):
        QThread.__init__(self)
        self.equipment_ni = equipment_ni
        while xbee.coordinator.is_open():
            time.sleep(0.1)
        xbee.open_coordinator_com()
        print("[INFO] Connection opened")

    def __del__(self):
        self.wait()

    def run(self):
        self.find_equipment(self.equipment_ni)

        # self.emit(SIGNAL('add_discovered_device(QList)'), devices)
        # self.sleep(0.5)

        self.signal_status.emit('finnished')
        xbee.close_coordinator_com()
        print("[INFO] Connection closed")


    def find_equipment(self, equipment_ni):
        """
            1) Descobrir a rede
            1) Recuperar todos os dispositivos
            1) Recuperar o dispositivo desejado na lista total
            1) Para cada dispositivo, comparar se MP == MY
            1) Caso (3) eh verdade, retorna em string o endereço de 64 bits do
                XBee que está conectado
            1) Consultar no banco de dados qual setor o XBee está associado
            1) Retornar a descrição do setor
        """
        status_found_devices = False
        xbee.discover_network() # Discovering network
        while xbee.xbee_network.is_discovery_running():
            self.signal_update_progress_bar.emit('loading')
            time.sleep(1.270)

        number_of_devices = xbee.get_all_devices()
        # xbee.xbee_network.clear()
        print("There are " + str(number_of_devices) + " connected")
        self.signal_number_of_connected_devices.emit(number_of_devices)

        try:
            xbee.find_equipment(equipment_ni)

            for d in xbee.all_devices:
                print(d)
                self.signal_update_progress_bar.emit('loading')
                xbee_64_bit_address = xbee.find_sector_by_equipment(d)
                if xbee_64_bit_address:
                    # If a device inside a sector was found, signal it
                    status_found_devices = True
                    print(xbee_64_bit_address)
                    self.signal_discovered_device.emit(xbee_64_bit_address)
                    break

            if not status_found_devices:
                # If no device inside a sector was found
                self.signal_discovered_device.emit("")

        except TimeoutException:
            self.signal_status.emit("busy")
        except InvalidOperatingModeException:
            print("InvalidOperatingModeException")

class DiscoverEquipmentsBySector(QThread):
    """
        Class used as a thread to discover every equipment inside an ambiente
        given an sector.
    """
    signal_status = pyqtSignal(str)
    signal_number_of_connected_devices = pyqtSignal(int)
    signal_discovered_device = pyqtSignal(str)
    signal_update_progress_bar = pyqtSignal(str)

    def __init__(self, device_name=""):
        QThread.__init__(self)
        self.device_name = device_name
        while xbee.coordinator.is_open():
            time.sleep(0.1)
        xbee.open_coordinator_com()
        print("[INFO] Connection opened")

    def __del__(self):
        self.wait()

    def run(self):
        print("[INFO] Thread started. Searching devices...")
        if self.device_name == 'Bioengenharia':
            self.find_equipment('R1')
        elif self.device_name == 'Enfermaria':
            self.find_equipment('R2')
        elif self.device_name == 'All':
            self.find_equipment('All')

        # self.emit(SIGNAL('add_discovered_device(QList)'), devices)
        # self.sleep(0.5)

        self.signal_status.emit('finnished')
        xbee.close_coordinator_com()
        print("[INFO] Connection closed")

    def find_equipment(self, sector):
        """
            1) Descobrir a rede
            2) Recuperar todos os dispositivos
            3) Para cada dispositivo, comparar se MP == MY
            4) Caso (3) eh verdade, retorna em string o endereço de 64 bits do
                XBee
            5) Consultar no banco de dados qual equipamento o XBee está
                associado
            6) Retornar a descrição do
        """
        status_found_devices = False
        xbee.discover_network() # Discovering network
        while xbee.xbee_network.is_discovery_running():
            self.signal_update_progress_bar.emit('loading')
            time.sleep(1.270)

        number_of_devices = xbee.get_all_devices()
        # xbee.xbee_network.clear()
        print("There are " + str(number_of_devices) + " connected")
        self.signal_number_of_connected_devices.emit(number_of_devices)

        try:

            if sector != 'All':
                xbee.find_router(sector)
                # Getting all equipment connected to the chosen sector
                # devices = xbee.get_sector_equipments(sector)
                for d in xbee.all_devices:
                    # print(d)
                    self.signal_update_progress_bar.emit('loading')
                    xbee_64_bit_address = xbee.compare_mp_my(d)
                    if xbee_64_bit_address:
                        # If a device inside a sector was found, signal it
                        status_found_devices = True
                        # print(xbee_64_bit_address)
                        self.signal_discovered_device.emit(xbee_64_bit_address)
            else:
                # returns all equipments
                for d in xbee.all_devices:
                    # print(d)
                    self.signal_update_progress_bar.emit('loading')
                    xbee_64_bit_address = xbee.get_equipment_64_bit_addr(d)
                    if xbee_64_bit_address:
                        # If a device inside a sector was found, signal it
                        status_found_devices = True
                        print(xbee_64_bit_address)
                        self.signal_discovered_device.emit(xbee_64_bit_address)



            if not status_found_devices:
                # If no device inside a sector was found
                self.signal_discovered_device.emit("")

        except TimeoutException:
            self.signal_status.emit("busy")
        except InvalidOperatingModeException:
            print("InvalidOperatingModeException")

def main():
    app = QApplication(sys.argv)
    form = LgpApp()
    form.show()
    if xbee.coordinator is None:
        print("Coordenador não encontrado")
        form.coordinator_not_found()
        form.close()
        app.exec_()
    else:
        app.exec_()


if __name__ == "__main__":
    xbee = xbee_handler.XBeeHandler()
    try:
        if xbee.coordinator is not None:
            pass
            print("Coordenador não encontrado.")
            # xbee.open_coordinator_com()
        main()
    finally:
        if xbee.coordinator is not None:
            if xbee.coordinator.is_open():
                xbee.close_coordinator_com()
                print("[INFO] Connection closed")
