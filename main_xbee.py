# Digi XBee Python library
#   https://github.com/digidotcom/python-xbee/tree/master/examples/network/DiscoverDevicesSample
# Get started with XBee Python library
#   http://xbplib.readthedocs.io/en/latest/getting_started_with_xbee_python_library.html
# Discover the XBee network
#   http://xbplib.readthedocs.io/en/latest/user_doc/discovering_the_xbee_network.html#
# digi.xbee.devices module
#   http://xbplib.readthedocs.io/en/latest/api/digi.xbee.devices.html

# PAN ID: C001BEE
# SC: FFF

# Corrdinator C: 13A200404A4BB3
# Router R1: 13A200404A4BC6
# Router R2: 13A200404AB737

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice, XBee64BitAddress

# Instanciando o coordenador
cordinator = XBeeDevice('/dev/ttyUSB0', 9600)
# Instanciando os roteadores
router_R1 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200404A4BC6"))
router_R2 = RemoteXBeeDevice(cordinator, XBee64BitAddress.from_hex_string("0013A200404AB737"))

# Abrindo conexao do C
cordinator.open()

if router_R1 == None:
    print("Router R1 not found!")
else:
    router_R1.read_device_info()
    router_64bit_addr = router_R1.get_16bit_addr();
    print(router_R1.get_node_id())
    print(router_64bit_addr.address)
    print(router_R1.get_parameter("MY"))


cordinator.close()
