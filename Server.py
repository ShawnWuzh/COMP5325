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
import time

import grpc

import ClientRequest_pb2
import ClientRequest_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(ClientRequest_pb2_grpc.GreeterServicer):

  def GetBalance(self, request, context):
    print("Check Balance")
    return ClientRequest_pb2.ClientResponse(responseAmt=2000)

  def Withdraw(self, request, context):
    print("Withdraw")
    FinalAmount = 2000 - request.requestAmt
    return ClientRequest_pb2.ClientResponse(responseAmt=FinalAmount)

  def Deposit(self, request, context):
    print("Deposit")
    FinalAmount = 2000 + request.requestAmt
    return ClientRequest_pb2.ClientResponse(responseAmt=FinalAmount)

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  ClientRequest_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
