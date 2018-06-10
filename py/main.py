from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time
import os

# PAN ID: C001BEE
# SC: FFF

# Cordinator C:    0013A200404A4BB3
# Router R1:        0013A200404A4BC6
# Router R2:        0013A200404AB737
# End Device 1:     0013A200407C48FE
# End Device 2:     0013A200407C48FF
# End Device 3:     0013A200407C4533
# End Device 4:     0013A200407C4927

# ----- DEVICES 64-bit ADDRESSES ---------------------------------
devices_64bit_addr = {
    "C": "0013A200404A4BB3",
    "R1": "0013A200404A4BC6",
    "R2":"0013A200404AB737",
    "E1": "0013A200407C48FE",
    "E2": "0013A200407C48FF",
    "E3": "0013A200407C4533",
    "E4": "0013A200407C4927"
}

# Instantiating the cordinator
cordinator = XBeeDevice('/dev/ttyUSB0', 9600)
# # Instantiating routers
# router_R1 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200404A4BC6"))
# router_R2 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200404AB737"))
# # Instantiating end devices
# end_dev_E1 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200407C48FE"))
# end_dev_E2 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200407C48FF"))
# end_dev_E3 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200407C4533"))
# end_dev_E4 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200407C4927"))

def readRouterEndDevices():
    """
        Returns a list of end devices conected to a specified router.

        Parameters
        --------
        None

        Returns
        --------
        List of RemoteXBeeDevice connected to a specified router if found and
        'None' in case of no end device connected.
    """

    router = input("> Enter the router NI (R1/R2): ")
    if router.title() == "R1":
        x64addr = XBee64BitAddress.from_hex_string(devices_64bit_addr['R1'])
    elif router.title() == "R2":
        x64addr = XBee64BitAddress.from_hex_string(devices_64bit_addr['R2'])
    else:
        print("Invalid NI. Try again.")
        return None

    print(f"Searching for devices in the network...")
    # Getting the xbee network
    xbee_network = cordinator.get_network()
    # Setting timeout
    xbee_network.set_discovery_timeout(25)
    xbee_network.start_discovery_process()
    while xbee_network.is_discovery_running():
        time.sleep(0.5)

    # Retrieving router from network by 64bit address
    print(f"Retrieving router '{router.title()}' in the network...")
    discovered_router = xbee_network.get_device_by_64(x64addr)
    if discovered_router is None:
        # If the device was not found
        print(f"Device {router} not found. Try again.")
        return None

    # If the device was found in the network
    print(f"Device {router.title()} found. Retrieving device information...")
    discovered_router.read_device_info()
    print(f"{router.title()}-NI: {discovered_router.get_node_id()}")

    print("Searching for EDs...")
    all_devices = xbee_network.get_devices()
    connected_ed = []
    for d in all_devices:
        d.read_device_info()
        if d.get_parameter("MP") == discovered_router.get_parameter("MY"):
            print(f"-{d.get_node_id()} connected.")
            connected_ed.append(d)

    if not connected_ed:
        # if the list connected_ed is empty
        print(f"No end device connected to router {router.title()}")
        return None
    else:
        return connected_ed


def menu():
    """Shows a menu with the Application Options.
    This function only shows the menu, you still need to gets the user inputs.
    """
    print('\n----------------------------- MENU ------------------------------')
    print('0 - EXIT PROGRAM ')
    print('1 - Read all router\'s EDs ')
    print('2 - Search for an ED ')
    print('C - CLEAR SCREEN *')
    print('-----------------------------------------------------------------\n')


def main():
    """
        Main Application
    """
    menu()

    while True:
        item = input(">>> SELECT AN OPTION: ")
        if item == '0' or item == 'q':
            break
        elif item == 'C' or item == 'c':
            os.system('cls' if os.name == 'nt' else 'clear')
            menu()
        elif item == '1':
            readRouterEndDevices();
            print('\n')
        else:
            print("Invalid option! Choose one option from the menu above.\n")

if __name__ == "__main__":
    try:
        cordinator.open()
        main()
    finally:
        print("Closing XBee connection...")
        cordinator.close()
        # while cordinator.isOpen():
        #     time.sleep(0.5)
        print("Connection successfully closed!")
