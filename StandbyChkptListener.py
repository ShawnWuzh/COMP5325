import threading
import socket
import sys
from BalanceHandler import BalanceHandler


class StandbyChkptListener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.handler = BalanceHandler()
        self.pause_cond = threading.Condition(threading.Lock())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', 19394)
        print ('starting up on %s port %s' % self.server_address)
        self.sock.bind(self.server_address)

    def run(self):
        while True:
            json_data, action_id = self.sock.recvfrom(4096)
            # implement actin ID checking
            self.handler.synchronize(json_data)