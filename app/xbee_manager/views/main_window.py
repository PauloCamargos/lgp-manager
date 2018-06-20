# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from .about import Ui_About
from .add_equipment import Ui_AddEquipment
from .list_equipment import Ui_ListEquipment
from .edit_equipment import Ui_EditEquipment
import sys

class Ui_MainWindow(object):
    # User methods
    # def open_version(self):
    #     # About window
    #     self.about_window = QtWidgets.QWidget()
    #     self.about = Ui_About()
    #     self.about.setupUi(self.about_window)
    #     self.about_window.show()

    # def open_add_equipment(self):
    #     # Add equipment window
    #     self.add_equipment_window = QtWidgets.QWidget()
    #     self.add_equipment = Ui_AddEquipment()
    #     self.add_equipment.setupUi(self.add_equipment_window)
    #     self.add_equipment_window.show()
    #
    # def open_list_equipment(self):
    #     # Add equipment window
    #     self.list_equipment_window = QtWidgets.QWidget()
    #     self.list_equipment = Ui_ListEquipment()
    #     self.list_equipment.setupUi(self.list_equipment_window)
    #     self.list_equipment_window.show()
    #
    # def open_edit_equipment(self):
    #     # Add equipment window
    #     self.edit_equipment_window = QtWidgets.QWidget()
    #     self.edit_equipment = Ui_EditEquipment()
    #     self.edit_equipment.setupUi(self.edit_equipment_window)
    #     self.edit_equipment_window.show()


    # Core methods
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(803, 579)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_5.addWidget(self.label_4)
        self.cbx_sector = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbx_sector.sizePolicy().hasHeightForWidth())
        self.cbx_sector.setSizePolicy(sizePolicy)
        self.cbx_sector.setObjectName("cbx_sector")
        self.cbx_sector.addItem("")
        self.cbx_sector.addItem("")
        self.horizontalLayout_5.addWidget(self.cbx_sector)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.list_devices = QtWidgets.QListWidget(self.groupBox)
        self.list_devices.setObjectName("list_devices")
        self.verticalLayout_4.addWidget(self.list_devices)
        self.btn_devices = QtWidgets.QPushButton(self.groupBox)
        self.btn_devices.setObjectName("btn_devices")
        self.verticalLayout_4.addWidget(self.btn_devices)
        self.horizontalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_4.addWidget(self.label_3)
        self.cbx_equipment = QtWidgets.QComboBox(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbx_equipment.sizePolicy().hasHeightForWidth())
        self.cbx_equipment.setSizePolicy(sizePolicy)
        self.cbx_equipment.setObjectName("cbx_equipment")
        self.cbx_equipment.addItem("")
        self.cbx_equipment.addItem("")
        self.cbx_equipment.addItem("")
        self.cbx_equipment.addItem("")
        self.horizontalLayout_4.addWidget(self.cbx_equipment)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.list_sector = QtWidgets.QListWidget(self.groupBox_2)
        self.list_sector.setObjectName("list_sector")
        self.verticalLayout_2.addWidget(self.list_sector)
        self.btn_sector = QtWidgets.QPushButton(self.groupBox_2)
        self.btn_sector.setObjectName("btn_sector")
        self.verticalLayout_2.addWidget(self.btn_sector)
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_6.addWidget(self.label_5)
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.horizontalLayout_6.addWidget(self.progress_bar)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 803, 25))
        self.menuBar.setObjectName("menuBar")
        self.menuArquivo = QtWidgets.QMenu(self.menuBar)
        self.menuArquivo.setObjectName("menuArquivo")
        self.menuEditar = QtWidgets.QMenu(self.menuBar)
        self.menuEditar.setObjectName("menuEditar")
        self.menuSobre = QtWidgets.QMenu(self.menuBar)
        self.menuSobre.setObjectName("menuSobre")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menu_avancado = QtWidgets.QAction(MainWindow)
        self.menu_avancado.setObjectName("menu_avancado")
        self.menu_sair = QtWidgets.QAction(MainWindow)
        self.menu_sair.setObjectName("menu_sair")
        self.menu_add_equipment = QtWidgets.QAction(MainWindow)
        self.menu_add_equipment.setObjectName("menu_add_equipment")

        # self.menu_add_equipment.triggered.connect(self.open_add_equipment)

        self.menu_list_equipment = QtWidgets.QAction(MainWindow)
        self.menu_list_equipment.setObjectName("menu_list_equipment")

        # self.menu_list_equipment.triggered.connect(self.open_list_equipment)

        self.menu_edit_equipment = QtWidgets.QAction(MainWindow)
        self.menu_edit_equipment.setObjectName("menu_edit_equipment")

        # self.menu_edit_equipment.triggered.connect(self.open_edit_equipment)

        self.menu_version = QtWidgets.QAction(MainWindow)
        self.menu_version.setObjectName("menu_version")

        # self.menu_version.triggered.connect(self.open_version)

        self.menu_help = QtWidgets.QAction(MainWindow)
        self.menu_help.setObjectName("menu_help")
        self.menuArquivo.addAction(self.menu_avancado)
        self.menuArquivo.addSeparator()
        self.menuArquivo.addAction(self.menu_sair)
        self.menuEditar.addAction(self.menu_add_equipment)
        self.menuEditar.addAction(self.menu_list_equipment)
        self.menuEditar.addAction(self.menu_edit_equipment)
        self.menuSobre.addAction(self.menu_version)
        self.menuSobre.addAction(self.menu_help)
        self.menuBar.addAction(self.menuArquivo.menuAction())
        self.menuBar.addAction(self.menuEditar.menuAction())
        self.menuBar.addAction(self.menuSobre.menuAction())

        self.retranslateUi(MainWindow)
        self.menu_sair.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Logah Manager"))
        self.groupBox.setTitle(_translate("MainWindow", "Por setor"))
        self.label_4.setText(_translate("MainWindow", "Setor:"))
        self.cbx_sector.setItemText(0, _translate("MainWindow", "Bioengenharia"))
        self.cbx_sector.setItemText(1, _translate("MainWindow", "Engenharia clínica"))
        self.label_2.setText(_translate("MainWindow", "Dispositivos encontrados:"))
        self.btn_devices.setText(_translate("MainWindow", "Buscar dispositivos"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Por equipamento"))
        self.label_3.setText(_translate("MainWindow", "Equipamento:"))
        self.cbx_equipment.setItemText(0, _translate("MainWindow", "Oxímetro"))
        self.cbx_equipment.setItemText(1, _translate("MainWindow", "Ventilador Mecânico "))
        self.cbx_equipment.setItemText(2, _translate("MainWindow", "Monitor Mutiparâmetro Portátil"))
        self.cbx_equipment.setItemText(3, _translate("MainWindow", "Ultrassom Portátil"))
        self.label.setText(_translate("MainWindow", "Setor encontrado:"))
        self.btn_sector.setText(_translate("MainWindow", "Buscar setor"))
        self.label_5.setText(_translate("MainWindow", "Status"))
        self.menuArquivo.setTitle(_translate("MainWindow", "Arquivo"))
        self.menuEditar.setTitle(_translate("MainWindow", "Editar"))
        self.menuSobre.setTitle(_translate("MainWindow", "Sobre"))
        self.menu_avancado.setText(_translate("MainWindow", "Avançado"))
        self.menu_sair.setText(_translate("MainWindow", "Sair"))
        self.menu_add_equipment.setText(_translate("MainWindow", "Adicionar equipamento"))
        self.menu_list_equipment.setText(_translate("MainWindow", "Listar equipamentos"))
        self.menu_edit_equipment.setText(_translate("MainWindow", "Editar equipamento"))
        self.menu_version.setText(_translate("MainWindow", "Versão"))
        self.menu_help.setText(_translate("MainWindow", "Ajuda"))


def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
