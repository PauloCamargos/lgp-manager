from xbee_manager import app
from xbee_manager import coordinator

coordinator.open()

try:
    root.mainloop()
finally:
    coordinator.close()
