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

"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import grpc
import sys

import ClientRequest_pb2
import ClientRequest_pb2_grpc

def lookup_balance(stub):
    acct_id = input("Enter your account ID: ")
    response = stub.GetBalance(ClientRequest_pb2.ClientRequest(acctId=acct_id))
    print("Current balance: " + str(response.responseAmt)+ "\n\n")

def withdrawal(stub):
    acct_id = input("Enter your account ID: ")
    amt = input("Enter amount your want to withdraw: ")
    response = stub.Withdraw(ClientRequest_pb2.ClientRequest(acctId=acct_id,requestAmt=int(amt)))
    print("Current balance: " + str(response.responseAmt) + "\n\n")

def deposit(stub):
    acct_id = input("Enter your account ID: ")
    amt = input("Enter amount your want to deposite: ")
    response = stub.Deposit(ClientRequest_pb2.ClientRequest(acctId=acct_id,requestAmt=int(amt)))
    print("Current balance: " + str(response.responseAmt)+ "\n\n")

def run():
  while (True):

    channel = grpc.insecure_channel('localhost:50051')
    stub = ClientRequest_pb2_grpc.GreeterStub(channel)

    print("---------------------------------------")
    print("* Enter you operation:                *")
    print("*    1: Look up balance               *")
    print("*    2: Withdraw an amount of money   *")
    print("*    3: Save an amount of money       *")
    print("*    4: Terminating program           *")
    print("---------------------------------------\n")

    op = input("Your choice: ")

    if op == "1":
      lookup_balance(stub)
    elif op == "2":
      withdrawal(stub)
    elif op == "3":
      deposit(stub)
    else:
      sys.exit()

    #response = stub.GetResult(ClientRequest_pb2.ClientRequest(actionType=username))
    #print("Greeter client received: " + str(response.responseAmt))

if __name__ == '__main__':
  run()
