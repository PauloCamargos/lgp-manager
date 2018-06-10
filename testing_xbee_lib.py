# Digi XBee Python library
#   https://github.com/digidotcom/python-xbee/tree/master/examples/network/DiscoverDevicesSample
# Get started with XBee Python library
#   http://xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html
# Discover the XBee network
#   http://xbplib.readthedocs.io/en/latest/user_doc/discovering_the_xbee_network.html#
# digi.xbee.devices module
#   http://xbplib.readthedocs.io/en/latest/api/digi.xbee.devices.html
# digi.xbee.models.address module
#   http://xbplib.readthedocs.io/en/latest/api/digi.xbee.models.address.html#digi.xbee.models.address.XBee16BitAddress

# PAN ID: C001BEE
# SC: FFF

# Corrdinator C:    0013A200404A4BB3
# Router R1:        0013A200404A4BC6
# Router R2:        0013A200404AB737
# End Device 1:     0013A200407C48FE
# End Device 2:     0013A200407C48FF
# End Device 3:     0013A200407C4533
# End Device 4:     0013A200407C4927


from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

cordinator_64bit_addr = "0013A200404A4BB3"
routers_64bit_addr = { "R1": "0013A200404A4BC6", " R2":"0013A200404AB737"}
end_devs_64bit_addr = {
    "E1": "0013A200407C48FE",
    "E2": "0013A200407C48FF",
    "E3": "0013A200407C4533",
    "E4": "0013A200407C4927"
}


# Instanciando o coordenador
cordinator = XBeeDevice('/dev/ttyUSB0', 9600)
# Instanciando os roteadores
router_R1 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200404A4BC6"))
router_R2 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200404AB737"))
end_dev_E1 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200407C48FE"))
end_dev_E2 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200407C48FF"))
end_dev_E3 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200407C4533"))
end_dev_E4 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200407C4927"))

# Abrindo conexao do C
try:

    cordinator.open()

    print("\n ------ Router info: ")

    if router_R1 == None:
        print("router_R1 not found!")
    else:
        router_R1.read_device_info()
        router_64bit_addr = router_R1.get_16bit_addr();
        print(router_R1.get_node_id())
        print(router_64bit_addr.address)
        print(router_R1.get_parameter("MY"))

    print("\n ------ End device info: ")

    if end_dev_E1 == None:
        print("end_dev_E1 not found!")
    else:
        end_dev_E1.read_device_info()
        end_dev_E1_64bit_addr = end_dev_E1.get_16bit_addr();
        print(end_dev_E1.get_node_id())
        print(end_dev_E1_64bit_addr.address)
        print(end_dev_E1.get_parameter("MP"))

    # c_network = cordinator.get_network()
    # c_network.set_discovery_timeout(25) # deixar um tempo razoave (~25s)
    # c_network.start_discovery_process()
    # while c_network.is_discovery_running():
    #     time.sleep(0.5)
    # x64addr = XBee64BitAddress.from_hex_string(end_devs_64bit_addr['E1'])
    # node_id = "E1"
    #
    # # e1 = c_network.get_devices()
    # e1 = c_network.discover_device(node_id)
    # # e1 = c_network.get_device_by_64(x64addr)
    # # e1 = c_network.get_device_by_node_id(node_id)
    # if e1 is None:
    #     print("Device not found")
    # else:
    #     print("Device found")
    #     e1.read_device_info()
    #     print(e1.get_node_id())

    #
    # def menu():
    #     """Shows a menu with the Application Options.
    #     This function only shows the menu, you still need to gets the user inputs.
    #     """
    #     print('\n----------------------------- MENU ------------------------------')
    #     print('0 - EXIT PROGRAM ')
    #     print('1 - Read SL Address ')
    #     print('C - CLEAR SCREEN *')
    #     print('-----------------------------------------------------------------\n')
    #
    # def main():
    #     """Main Application
    #     """
    #     menu()
    #
    #     while True:
    #         item = input(">>> SELECT AN OPTION: ")
    #         if item == '0' or item == 'q':
    #             comport.close()
    #             break
    #         elif item == 'C' or item == 'c':
    #             os.system('cls' if os.name == 'nt' else 'clear')
    #             menu()
    #         elif item == '1':
    #             readSL();
    #         else:
    #             print("Invalid option! Choose one option from the menu above.\n")
    #
    #
    # if __name__ == '__main__':
    #     main()
finally:
    cordinator.close()
