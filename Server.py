# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures
from threading import Thread
import time
import json
import socket
import grpc
import ClientRequest_pb2
import ClientRequest_pb2_grpc

from BalanceHandler import BalanceHandler
from GlobVar import Globvar
from StandbyChkptListener import StandbyChkptListener

class Greeter(ClientRequest_pb2_grpc.GreeterServicer):
  def __init__(self):
    self.balance_handler = BalanceHandler()
    self.current_balance = None
    self.addr_list = None
    with open("serverhost.config", 'r') as server_data:
      # TODO: Get the correct peer server address
      self.addr_list =json.load(server_data)
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP


  def GetBalance(self, request, context):
    print("{0} Server Check Balance".format(Globvar.SERVER_STATUS))
    if Globvar.SERVER_STATUS != "PRIMARY":
      return ClientRequest_pb2.ClientResponse(status="REJECT", actionId=Globvar.ACTION_ID,
                                              acctId=request.acctId, responseAmt=self.current_balance)
    result = self.balance_handler.lookup_balance(request.acctId)
    if result != "Account not found":
      self.current_balance = result
      # TODO: send to the correct peer server
      self.sock.sendto(self.balance_handler.serialization(), (self.addr_list["s2"], Globvar.SYNC_PORT))
      Globvar.ACTION_ID += 1
      return ClientRequest_pb2.ClientResponse(status="SUCCESS", actionId=Globvar.ACTION_ID,
                                              acctId=request.acctId, responseAmt=self.current_balance)
    else:
      return ClientRequest_pb2.ClientResponse(status=result, actionId=Globvar.ACTION_ID,
                                              acctId=request.acctId, responseAmt=self.current_balance)

  def Withdraw(self, request, context):
    print("{0} Server Withdraw".format(Globvar.SERVER_STATUS))
    if Globvar.SERVER_STATUS != "PRIMARY":
      return ClientRequest_pb2.ClientResponse(status="REJECT", actionId=Globvar.ACTION_ID,
                                              acctId=request.acctId, responseAmt=self.current_balance)

    result = self.balance_handler.withdraw(request.requestAmt)
    if result == "SUCCESS":
      # TODO: send to the correct peer server
      self.sock.sendto(self.balance_handler.serialization(), (self.addr_list["s2"], Globvar.SYNC_PORT))
      Globvar.ACTION_ID += 1

    self.current_balance = self.balance_handler.lookup_balance(request.acctId)
    return ClientRequest_pb2.ClientResponse(status=result, actionId=Globvar.ACTION_ID,
                                              acctId=request.acctId, responseAmt=self.current_balance)

  def Deposit(self, request, context):
    print("{0} Server Deposit".format(Globvar.SERVER_STATUS))
    if Globvar.SERVER_STATUS != "PRIMARY":
      return ClientRequest_pb2.ClientResponse(status="REJECT", actionId=Globvar.ACTION_ID,
                                              acctId=request.acctId, responseAmt=self.current_balance)

    result = self.balance_handler.deposit(request.requestAmt)
    if result == "SUCCESS":
      # TODO: send to the correct peer server
      self.sock.sendto(self.balance_handler.serialization(), (self.addr_list["s2"], Globvar.SYNC_PORT))
      Globvar.ACTION_ID += 1

    self.current_balance = self.balance_handler.lookup_balance(request.acctId)
    return ClientRequest_pb2.ClientResponse(status=result, actionId=Globvar.ACTION_ID,
                                              acctId=request.acctId, responseAmt=self.current_balance)


def serve():
  sync_listener = StandbyChkptListener()
  sync_listener.start()
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  ClientRequest_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(Globvar._ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    #TODO: handle thread stop for listener
    server.stop(0)


if __name__ == '__main__':
  serve()
