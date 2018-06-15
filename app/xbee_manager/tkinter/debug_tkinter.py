from xbee_manager import app
from xbee_manager import coordinator


try:
    coordinator.open()
    app.mainloop()
finally:
    coordinator.close()
