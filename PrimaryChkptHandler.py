import threading
import socket
import sys
import json
import time
from BalanceHandler import BalanceHandler
from GlobVar import Globvar


class PrimaryChkptHandler(threading.Thread):
  def __init__(self, balance_handler):
    super(PrimaryChkptHandler, self).__init__()
    self.addr_list = None
    self._stop_event = threading.Event()
    self.handler = balance_handler
    self.pause_cond = threading.Condition(threading.Lock())
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    with open('./serverhost.config') as sever_data:
      self.addr_list = json.load(sever_data)

  def run(self):
    while True:
      if self._stop_event.is_set():
        break
      time.sleep(Globvar.CHECKPOINT_DURATION)
      self.sock.sendto(self.handler.serialization(), (self.addr_list["s2"], Globvar.SYNC_PORT))



  def stop(self):
    self._stop_event.set()

  def stopped(self):
    return self._stop_event.is_set()

if __name__ == "__main__":
  server = PrimaryChkptHandler()
  server.run()