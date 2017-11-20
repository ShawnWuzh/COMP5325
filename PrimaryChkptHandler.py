import threading
import socket
import sys
import json
from BalanceHandler import BalanceHandler
from GlobVar import Globvar


class PrimaryChkptHandler(threading.Thread):
  def __init__(self):
    super(PrimaryChkptHandler, self).__init__()
    self._stop_event = threading.Event()
    self.handler = BalanceHandler()
    self.pause_cond = threading.Condition(threading.Lock())
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.server_address = ('localhost', Globvar.SYNC_PORT)

  def run(self):
    while True:
      if self._stop_event.is_set():
        break
      # TODO: send to the correct peer server
      self.sock.sendto(self.balance_handler.serialization(), (self.addr_list["s2"], Globvar.SYNC_PORT))


  def stop(self):
    self._stop_event.set()

  def stopped(self):
    return self._stop_event.is_set()

if __name__ == "__main__":
  server = PrimaryChkptHandler()
  server.run()