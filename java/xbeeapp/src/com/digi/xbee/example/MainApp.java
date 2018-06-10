package com.digi.xbee.example;

import java.io.Reader;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

import com.digi.xbee.api.RemoteXBeeDevice;
import com.digi.xbee.api.XBeeDevice;
import com.digi.xbee.api.exceptions.XBeeException;
import com.digi.xbee.api.models.XBee64BitAddress;
import com.digi.xbee.api.XBeeNetwork;

public class MainApp {
	/* MESH MAIN INFORMATION */
	// PAN ID: C001BEE
	// SC: FFF
	/* 64-BIT ADDRESSES */
	// coordinator C: 0013A200404A4BB3
	// Router R1: 0013A200404A4BC6
	// Router R2: 0013A200404AB737
	// End Device 1: 0013A200407C48FE
	// End Device 2: 0013A200407C48FF
	// End Device 3: 0013A200407C4533
	// End Device 4: 0013A200407C4927
	/* Constants */
	// TODO Replace with the port where your sender module is connected to.
	private static final String PORT = "/dev/ttyUSB0";
	// TODO Replace with the baud rate of your sender module.
	private static final int BAUD_RATE = 9600;

	public static void main(String[] args) {
		Scanner reader = new Scanner(System.in);
		XBeeDevice coordinator = new XBeeDevice(PORT, BAUD_RATE); // Instantiating the local (coordinator) device
		String device_name; // Holds the option for device [R1,R2,E1...]
		String device_address = ""; // Holds the 64-bit address for the chosen device

		// Dictionary holding the device name and its 64-bit address
		Map<String, String> devices64bitAdrresses = new HashMap<String, String>();
		devices64bitAdrresses.put("C", "0013A200404A4BB3");
		devices64bitAdrresses.put("R1", "0013A200404A4BC6");
		devices64bitAdrresses.put("R2", "0013A200404AB737");
		devices64bitAdrresses.put("E1", "0013A200407C48FE");
		devices64bitAdrresses.put("E2", "0013A200407C48FF");
		devices64bitAdrresses.put("E3", "0013A200407C4533");
		devices64bitAdrresses.put("E4", "0013A200407C4927");

		try {
			coordinator.open(); // Opening connection with the coord.
			XBeeNetwork xbee_network = coordinator.getNetwork(); // Retrieving is network
			RemoteXBeeDevice router = null;
			int option = -1;

			// Menu
			System.out.println(" ------------------------ MENU ------------------------");
			System.out.println(" 0 - Quit the program ");
			System.out.println(" 1 - Read all router's EDs ");
			System.out.println(" 2 - Search for device ");
			System.out.println(" * 3 - Get the number of remote devs. ");
			System.out.println(" * 4 - Get a parameter [MP, MY, SL...] ");
			System.out.println("-------------------------------------------------------");

			while (option != 0) {
				System.out.print(">>> Enter your option: ");

				option = reader.nextInt();

				switch (option) {
				case 0: // Exit
					option = 0;
					break;
				case 1: // Reads all router's EDs
					System.out.print("Enter the device name [R1,R2]: ");
					device_name = reader.next();
					device_address = "";
					switch (device_name) {
					case "R1":
						device_address = devices64bitAdrresses.get(device_name); // Retrieving the 64-bit addr. from the
																					// List
						break;
					case "R2":
						device_address = devices64bitAdrresses.get(device_name); // Retrieving the 64-bit addr. from the
																					// List
						break;
					default:
						System.out.println("Device name not valid. Try again.\n"); // If the value typed wasn't valid
						break;
					}
					
					if(device_address.equals(""))
						break;

					System.out.println("Starting discover process...");
					xbee_network.setDiscoveryTimeout(10000); // Estabilishing a timeout in ms
					xbee_network.startDiscoveryProcess();

					// Holding the program until the startDiscoveryProcess() has not been finished
					while (xbee_network.isDiscoveryRunning()) {
						// Do nothing until disc. is finished
						try {
							TimeUnit.SECONDS.sleep(1);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
						;
					}

					System.out.println("Discover process finished.");

					router = xbee_network.getDevice(new XBee64BitAddress(device_address)); // Getting a specific device
																							// from the network

					if (router == null) { // Case the router was NOT found
						System.out.println("The specified router was not found. Try again.\n");
						break;
					} else { // Case the router was found
						System.out.println("Router NI: " + router.getNodeID()); // Show the chosen router NI parameter

						List<RemoteXBeeDevice> remotes = xbee_network.getDevices(); // List holding all remote devices,
																					// including the router
						Map<String, RemoteXBeeDevice> ed_children = new HashMap<String, RemoteXBeeDevice>(); // List
																												// with
																												// every
																												// router's
																												// children

						for (RemoteXBeeDevice dev : remotes) { // Loop to check if a device's MP = MY
							// System.out.println("Remote: " + devs.getNodeID()); //DEBUG
							if (dev.getParameter("MP") == router.getParameter("MY")) { // If MP == MY
								ed_children.put(dev.getNodeID(), dev); // Save that device with it's NI and itself
							}
						}
						if (ed_children.isEmpty()) { // If no children device was found
							System.out.println("No children devices was found.");
							System.out.println();
						} else { // If it has, print all children ED node identifier NI
							System.out.println("Children node found: ");
							Iterator it = ed_children.entrySet().iterator();
							while (it.hasNext()) {
								Map.Entry pair = (Map.Entry) it.next();
								System.out.println(pair.getKey());
							}
						}
					}
					break;

				case 2:
					System.out.print("Enter the device name [R1,R2,E1,E2,E3,E4]: ");
					device_name = reader.next();
					device_address = "";
					switch (device_name) {
					case "R1":
						device_address = devices64bitAdrresses.get(device_name); // Retrieving the 64-bit addr. from the
																					// List
						break;
					case "R2":
						device_address = devices64bitAdrresses.get(device_name);
						break;
					case "E1":
						device_address = devices64bitAdrresses.get(device_name);
						break;
					case "E2":
						device_address = devices64bitAdrresses.get(device_name);
						break;
					case "E3":
						device_address = devices64bitAdrresses.get(device_name);
						break;
					case "E4":
						device_address = devices64bitAdrresses.get(device_name);
						break;
					default:
						System.out.println("Device name not valid. Try again.\n");
						break;

					}

					if(device_address.equals(""))
						break;
					
					System.out.println("Starting discover process...");
					xbee_network.setDiscoveryTimeout(10000); // Estabilishing a timeout in ms
					xbee_network.startDiscoveryProcess();

					// Holding the program until the startDiscoveryProcess() has not been finished
					while (xbee_network.isDiscoveryRunning()) {
						// Do nothing until disc. is finished
						try {
							TimeUnit.SECONDS.sleep(1);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						}
						;
					}

					System.out.println("Discover process finished.");

					router = xbee_network.getDevice(new XBee64BitAddress(device_address)); // Getting a specific device
																							// from the network

					if (router == null) { // If the device wasn't found
						System.out.println("The specified device was not found. Try again.\n");
						System.out.println();
						break;
					} else { // If the device was found, print its NI
						System.out.println("[OK] Device found in the network.");
						System.out.println("Device NI: " + router.getNodeID());
						System.out.println();
					}
					break;
				default:
					System.out.println("Invalid option. Try again.\n");
					System.out.println();
					break;
				}
			}
			reader.close();

		} catch (XBeeException e) {
			System.out.println(" >> Error");
			e.printStackTrace();
			System.exit(1);
		} finally {
			System.out.println("Closing connection...");
			coordinator.close();
			while (coordinator.isOpen()) {
				// Wait
			}
			System.out.println("Connection closed with success.");
		}
	}
}
