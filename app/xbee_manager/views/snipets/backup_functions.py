

def open_add_equipment(self):
  # Add equipment window
  self.add_equipment_window = QtWidgets.QWidget()
  self.ui = Ui_AddEquipment()
  self.ui.setupUi(self.add_equipment_window)
  self.add_equipment_window.show()

  # self.menu_add_equipment.triggered.connect(self.open_add_equipment)

def open_list_equipment(self):
  # Add equipment window
  self.list_equipment_window = QtWidgets.QWidget()
  self.ui = Ui_ListEquipment()
  self.ui.setupUi(self.list_equipment_window)
  self.list_equipment_window.show()

  # self.menu_list_equipment.triggered.connect(self.open_list_equipment)

def open_version(self, window_name=""):
  # About window
  self.about_window = QtWidgets.QWidget()
  self.ui = Ui_About()
  self.ui.setupUi(self.about_window)
  self.about_window.show()

  #  self.menu_version.triggered.connect(self.open_version)
