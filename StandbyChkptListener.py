import threading
import socket
import sys
import json
from BalanceHandler import BalanceHandler
from GlobVar import Globvar


class StandbyChkptListener(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.handler = BalanceHandler()
    self.pause_cond = threading.Condition(threading.Lock())
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.server_address = ('localhost', Globvar.SYNC_PORT)
    print ('starting up on %s port %s' % self.server_address)
    self.sock.bind(self.server_address)

  def run(self):
    while True:
      # TODO: handle thread termination
      data, server = self.sock.recvfrom(4096)
      datalist = data.decode("utf-8").split(";")
      json_data = json.loads(datalist[0])
      actionId = int(datalist[1])
      if actionId > Globvar.ACTION_ID:
        Globvar.ACTION_ID = actionId
        self.handler.synchronize(json_data)

  #TODO: handle thread termination

if __name__ == "__main__":
  server = StandbyChkptListener()
  server.run()