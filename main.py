from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress
import time
import os

# ----- DEVICES INITIALIZATIONS ---------------------------------
cordinator_64bit_addr = "0013A200404A4BB3"
routers_64bit_addr = { "R1": "0013A200404A4BC6", " R2":"0013A200404AB737"}
end_devs_64bit_addr = {
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
    router = input("Enter the router NI (R1/R2): ")
    if router == "R1":
        x64addr = XBee64BitAddress.from_hex_string("0013A200404A4BC6")
    elif router == "R2":
        x64addr = XBee64BitAddress.from_hex_string("0013A200404A4BC6")
    else:
        print("Invalid NI. Try again.")
        return None

    # Getting the xbee network
    xbee_network = cordinator.get_network()
    # Setting timeout
    xbee_network.set_discovery_timeout(20)
    print(f"Searching for router {router} in the network...")
    xbee_network.start_discovery_process()
    while xbee_network.is_discovery_running():
        time.sleep(0.5)

    # Retrieving router from network by 64bit address
    discovered_router = xbee_network.get_device_by_64(x64addr)
    if discovered_router is None:
        # If the device was not found
        print(f"Device {router} not found. Try again.")
        return None

    # If the device was found in the network
    print(f"Device {router} found. Retrieving device information...")







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
    """Main Application
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
        print("Connection successfully closed!")
