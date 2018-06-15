from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress, DiscoveryOptions
import time
import os
import sys
import glob
import serial

class XBeeHandler():
    """
    Class to handle XBee's methods. It integrates easily with the LOGAH Manager
    GUI.
    """

    def __init__(self):
        self.devices_64bit_addr = {
            "C": "0013A200404A4BB3",
            "R1": "0013A200404A4BC6",
            "R2":"0013A200404AB737",
            "E1": "0013A200407C48FE",
            "E2": "0013A200407C48FF",
            "E3": "0013A200407C4533",
            "E4": "0013A200407C4927"
        }
        self.open_ports = self.serial_ports()
        self.coordinator = XBeeDevice(self.open_ports[0], 9600)


    def openCoordinatorCom(self):
        """
        Opens the communication with the local XBee
        """
        self.coordinator.open()


    def closeCoordinatorCom(self):
        """
        Closes the communication with the local XBee
        """
        self.coordinator.close()

    def getSectorEquipments(self, sector):
        """
            Returns a list of end devices conected to a specified router.

            Parameters
            --------
            String: The device name, such as 'R1' or 'R2'.

            Returns
            --------
            List of RemoteXBeeDevice connected to a specified router if found
            and 'None' in case of no end device connected.
        """

        if sector.title() == "R1":
            x64addr = XBee64BitAddress.from_hex_string(self.devices_64bit_addr['R1'])
        elif sector.title() == "R2":
            x64addr = XBee64BitAddress.from_hex_string(self.devices_64bit_addr['R2'])
        else:
            print("Invalid sector. Try again.")
            return None

        print(f"Searching for devices in the network...")
        # Getting the xbee network
        xbee_network = self.coodinator.get_network()
        # discovery options
        xbee_network.set_discovery_options({DiscoveryOptions.APPEND_DD})

        # Setting timeout
        xbee_network.set_discovery_timeout(5)
        xbee_network.start_discovery_process()
        # while xbee_network.is_discovery_running():
            # time.sleep(0.5)

        if not xbee_network.is_discovery_running():
        # Retrieving router from network by 64bit address
            print(f"Retrieving router '{sector.title()}' in the network...")
            discovered_device = xbee_network.get_device_by_64(x64addr)
            if discovered_device is None:
                # If the device was not found
                print(f"Device {router} not found. Try again.")
                xbee_network.clear()
                return None

            # If the device was found in the network
            print(f"Device {sector.title()} found. Retrieving device information...")
            discovered_device.read_device_info()
            print(f"{sector.title()}-NI: {discovered_device.get_node_id()}")
            print("Searching for EDs...")

            all_devices = xbee_network.get_devices() # Get network's devices
            xbee_network.clear() # Clearing the network before new discovery
            print("Devices: " + str(len(all_devices)))
            print("Devices type: " + str(discovered_device.get_parameter("DD")))
            connected_ed = []

            for d in all_devices:
                d.read_device_info()
                mp = str(d.get_parameter("MP"))
                # if ==
                my = str(discovered_device.get_parameter("MY"))
                print("MP encontado: " + mp +" | " + my)
                # print(f"-Router{d.get_node_id()} FOUND.")
                if mp == my:
                    print(f"-{d.get_node_id()} connected.")
                    connected_ed.append(d.get_node_id())
            if not connected_ed:
                # if the list connected_ed is empty
                print(f"No other device connected to device {sector.title()}")
                return None
            else:
                return connected_ed


    def getEquipmentLocation(self, equipment):
        """
            Searches the router (sector) which an specified equipment
            (end device) is located.

            Parameters
            --------
            String: The equipment name, such as 'Oxímetro'.

            Returns
            --------
            RemoteXBeeDevice: The router (sector) which an specified equipment
            (end device) is connectd.
        """
        if equipment.title() == "E1":
            x64addr = XBee64BitAddress.from_hex_string(self.devices_64bit_addr['E1'])
        elif equipment.title() == "E2":
            x64addr = XBee64BitAddress.from_hex_string(self.devices_64bit_addr['E2'])
        elif equipment.title() == "E3":
            x64addr = XBee64BitAddress.from_hex_string(self.devices_64bit_addr['E3'])
        elif equipment.title() == "E4":
            x64addr = XBee64BitAddress.from_hex_string(self.devices_64bit_addr['E4'])
        else:
            print("Invalid sector. Try again.")
            return None

        print(f"Searching for devices in the network...")
        # Getting the xbee network
        xbee_network = self.coodinator.get_network()
        # discovery options
        xbee_network.set_discovery_options({DiscoveryOptions.APPEND_DD})

        # Setting timeout
        xbee_network.set_discovery_timeout(5)
        xbee_network.start_discovery_process()
        while xbee_network.is_discovery_running():
            time.sleep(0.5)

        # Retrieving router from network by 64bit address
        print(f"Retrieving router '{equipment.title()}' in the network...")
        discovered_device = xbee_network.get_device_by_64(x64addr)
        if discovered_device is None:
            # If the device was not found
            print(f"Device {equipment} not found. Try again.")
            xbee_network.clear()
            return None

        # If the device was found in the network
        print(f"Device {equipment.title()} found. Retrieving device information...")
        discovered_device.read_device_info()
        print(f"{equipment.title()}-NI: {discovered_device.get_node_id()}")
        print("Searching for EDs...")

        all_devices = xbee_network.get_devices() # Get network's devices
        xbee_network.clear() # Clearing the network before new discovery
        print("Devices: " + str(len(all_devices)))
        print("Devices type: " + str(discovered_device.get_parameter("DD")))

        end_device = None

        for d in all_devices:
            d.read_device_info()
            mp = str(d.get_parameter("MP"))
            # if ==
            my = str(discovered_device.get_parameter("MY"))
            print("MP encontado: " + mp +" | " + my)
            # print(f"-Router{d.get_node_id()} FOUND.")
            if mp == my:
                print(f"-{d.get_node_id()} connected.")
                end_device = d.get_node_id()
        if not end_device:
            # if the list connected_ed is empty
            print(f"No other device connected to device {equipment.title()}")
            return None
        else:
            return connected_ed


    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result


if __name__ == '__main__':
    # print(serial_ports())
    my_device = XBeeHandler()