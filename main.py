import psycopg2
import serial
import time
import os
import serial.tools.list_ports

print('Estou funcionando!')

arduino_port = serial.tools.list_ports.comports()[0].device
print(f"Found Arduindo at port {port_name}")
comport = serial.Serial(arduino_port, 9600, timeout=5)


def readSL():
    """
    Sends a request askign for the SL number of a Xbee Device.

    Returns
    -------
    String: If the device was found, returns a string representing the XBee's SL
    address. If the divice wasn't found, returns 'None'.

    """

    end_device = input("Enter the End Device number: ")
    print(f"Sending request to Arduino for End Device number {end_device}...")
    comport.write(end_device)
    time.sleep(1.8)
    value_serial = comport.readline()
    
    if value_serial == '0':
        # If not found
        print("The specified device was not found")
        return None
    else:
        print(f"Device with SL number {value_serial} found.")
        return value_serial


def menu():
    """Shows a menu with the Application Options.
    This function only shows the menu, you still need to gets the user inputs.
    """
    print('\n----------------------------- MENU ------------------------------')
    print('0 - EXIT PROGRAM ')
    print('1 - Read SL Address ')
    print('C - CLEAR SCREEN *')
    print('-----------------------------------------------------------------\n')

def main():
    """Main Application
    """
    menu()

    while True:
        item = input(">>> SELECT AN OPTION: ")
        if item == '0' or item == 'q':
            comport.close()
            break
        elif item == 'C' or item == 'c':
            os.system('cls' if os.name == 'nt' else 'clear')
            menu()
        elif item == '1':
            readSL();
        else:
            print("Invalid option! Choose one option from the menu above.\n")


if __name__ == '__main__':
    main()
