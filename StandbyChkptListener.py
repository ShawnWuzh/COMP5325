import threading
import socket
import sys
import json
from BalanceHandler import BalanceHandler
from GlobVar import Globvar


class StandbyChkptListener(threading.Thread):
  def __init__(self, balance_handler):
    super(StandbyChkptListener, self).__init__()
    self.addr_list = None
    self._stop_event = threading.Event()
    self.handler = balance_handler
    self.pause_cond = threading.Condition(threading.Lock())
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.sock.settimeout(Globvar.CHECKPOINT_DURATION * 2)
    with open('./serverhost.config') as sever_data:
      self.addr_list = json.load(sever_data)
    self.server_address = (self.addr_list['s1'], Globvar.SYNC_PORT)
    print('starting up on %s port %s' % self.server_address)
    self.sock.bind(self.server_address)

  def run(self):
    while True:
      if self._stop_event.is_set():
        break
      try:
        data, server = self.sock.recvfrom(4096)
        print("data received")
        datalist = data.decode("utf-8").split(";")
        json_data = json.loads(datalist[0])
        action_id = int(datalist[1])
        print("received action id")
        self.handler.synchronize(json_data, action_id)
      except Exception as e:
        print("Receive timeout")
        continue
    print("standby sync socket thread is closed")

  def stop(self):
      self.sock.shutdown(socket.SHUT_RDWR)
      print("Shut down standby sync socket")
      self._stop_event.set()
      print("Shut down standby sync socket thread")

  def stopped(self):
      return self._stop_event.is_set()

if __name__ == "__main__":
  server = StandbyChkptListener()
  server.run()