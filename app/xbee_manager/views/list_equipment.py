# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'list_equipment.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ListEquipment(object):
    def setupUi(self, ListEquipment):
        ListEquipment.setObjectName("ListEquipment")
        ListEquipment.resize(1000, 474)
        ListEquipment.setMinimumSize(QtCore.QSize(1000, 474))
        ListEquipment.setMaximumSize(QtCore.QSize(1000, 474))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ListEquipment)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(ListEquipment)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.list_registered_equipment = QtWidgets.QListWidget(self.groupBox)
        self.list_registered_equipment.setObjectName("list_registered_equipment")
        self.verticalLayout_5.addWidget(self.list_registered_equipment)
        self.horizontalLayout_4.addWidget(self.groupBox)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(ListEquipment)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.list_found_equipment = QtWidgets.QListWidget(self.groupBox_2)
        self.list_found_equipment.setObjectName("list_found_equipment")
        self.verticalLayout_6.addWidget(self.list_found_equipment)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(ListEquipment)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        self.progress_bar = QtWidgets.QProgressBar(ListEquipment)
        self.progress_bar.setProperty("value", 24)
        self.progress_bar.setObjectName("progress_bar")
        self.horizontalLayout_6.addWidget(self.progress_bar)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.bnt_list_equipment = QtWidgets.QPushButton(ListEquipment)
        self.bnt_list_equipment.setMinimumSize(QtCore.QSize(400, 0))
        self.bnt_list_equipment.setMaximumSize(QtCore.QSize(355, 16777215))
        self.bnt_list_equipment.setObjectName("bnt_list_equipment")
        self.verticalLayout_4.addWidget(self.bnt_list_equipment, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(ListEquipment)
        QtCore.QMetaObject.connectSlotsByName(ListEquipment)

    def retranslateUi(self, ListEquipment):
        _translate = QtCore.QCoreApplication.translate
        ListEquipment.setWindowTitle(_translate("ListEquipment", "Visualizar todos equipamentos"))
        self.groupBox.setTitle(_translate("ListEquipment", "Equipamentos Cadastrados"))
        self.groupBox_2.setTitle(_translate("ListEquipment", "Equipamentos encontrados"))
        self.label.setText(_translate("ListEquipment", "Status"))
        self.bnt_list_equipment.setText(_translate("ListEquipment", "Listar Equipamentos"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ListEquipment = QtWidgets.QWidget()
    ui = Ui_ListEquipment()
    ui.setupUi(ListEquipment)
    ListEquipment.show()
    sys.exit(app.exec_())
