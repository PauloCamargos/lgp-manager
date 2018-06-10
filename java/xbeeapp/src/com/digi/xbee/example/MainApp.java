package com.digi.xbee.example;

import java.io.Reader;
import java.util.List;
import java.util.Scanner;
import java.util.concurrent.TimeUnit;

import com.digi.xbee.api.RemoteXBeeDevice;
import com.digi.xbee.api.XBeeDevice;
import com.digi.xbee.api.exceptions.XBeeException;
import com.digi.xbee.api.models.XBee64BitAddress;
import com.digi.xbee.api.XBeeNetwork;

public class MainApp {
	// PAN ID: C001BEE
	// SC: FFF

	// coordinator C: 0013A200404A4BB3
	// Router R1: 0013A200404A4BC6
	// Router R2: 0013A200404AB737
	// End Device 1: 0013A200407C48FE
	// End Device 2: 0013A200407C48FF
	// End Device 3: 0013A200407C4533
	// End Device 4: 0013A200407C4927
	/* Constants */
	// TODO Replace with the port where your sender module is connected to.
	private static final String PORT = "/dev/ttyUSB2";
	// TODO Replace with the baud rate of your sender module.
	private static final int BAUD_RATE = 9600;

	private static final String DATA_TO_SEND = "Hello XBee World!";

	public static void main(String[] args) {
		Scanner reader = new Scanner(System.in);

		XBeeDevice coordinator = new XBeeDevice(PORT, BAUD_RATE);

		byte[] dataToSend = DATA_TO_SEND.getBytes();

		try {
			coordinator.open();
			XBeeNetwork xbee_network = coordinator.getNetwork();

			int option = -1;
			
			System.out.println(" ------------------------ MENU ------------------------");
			System.out.println(" 0 - Quit the program ");
			System.out.println(" 1 - Search for device ");
			System.out.println(" 2 - ");
			System.out.println("-------------------------------------------------------");

			while (option != 0) {
				System.out.print(">>> Enter your option: ");
				
				option = reader.nextInt();

				switch (option) {
				case 0:
					option = 0;
					break;
				case 1:
					System.out.println("Starting discover process...");
					xbee_network.setDiscoveryTimeout(10000); // ms

					xbee_network.startDiscoveryProcess();
					while (xbee_network.isDiscoveryRunning()) {
						// Do nothing until disc. is finished
						try {
							TimeUnit.SECONDS.sleep(1);
						} catch (InterruptedException e) {
							// TODO Auto-generated catch block
							e.printStackTrace();
						};
					}
					
					// List<RemoteXBeeDevice> remotes = xbee_network.getDevices();
					System.out.println("Discover process finished.");
					RemoteXBeeDevice router = xbee_network.getDevice(new XBee64BitAddress("0013A200404A4BC6"));
					
					if (router == null) {
						System.out.println("The specified device was not found. Try again.");
						break;
					} else {
						System.out.println("[OK] Device found in the network.");
						System.out.println("Device NI: " + router.getNodeID());
						System.out.println();
					}
					break;
				default:
					System.out.println("Invalid option. Try again.");
					System.out.println();
					break;
				}
			}
			reader.close();


//			System.out.format("Sending broadcast data: '%s'", new String(dataToSend));
//
//			coordinator.sendBroadcastData(dataToSend);

		} catch (XBeeException e) {
			System.out.println(" >> Error");
			e.printStackTrace();
			System.exit(1);
		} finally {
			System.out.println("Closing connection...");
			coordinator.close();
			while(coordinator.isOpen()) {
				// Wait
			}
			System.out.println("Connection closed with success.");
		}
	}
}