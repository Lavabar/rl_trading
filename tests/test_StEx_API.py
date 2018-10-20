import time
import threading
import sys
sys.path.append("../")

from MyWrapper import MyWrapper
from ibapi.client import EClient

# two base classes for working with tws API
tws = EClient(MyWrapper())

# connecting to tws(it should be launched beforehand)
# localhost:7497, clientID = 1
tws.connect("127.0.0.1", 7497, 1)

if tws.isConnected():
    print("Connected!")
    # start listenning from tws in another thread
    tws.th = threading.Thread(target=tws.run)
    tws.th.start()
    tws.th.join(timeout=5)

    # waiting for messages from tws
    time.sleep(10)

    # disconnection procedure
    tws.done = True
    while tws.done and not tws.wrapper.end_work_with_TWS:
        print("Waiting for terminal switching off")
        time.sleep(0.5)
