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
import json


import grpc
import sys
import time
import os
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
  with open('./serverhost.config') as sever_data:
    addr_list = json.load(sever_data)
  primary = 's1'
  while (True):
    try:
      channel = grpc.insecure_channel('{}:50051'.format(addr_list[primary]))
      stub = ClientRequest_pb2_grpc.GreeterStub(channel)
    except:
      if primary == 's1':
        primary = 's2'
      else:
        primary = 's1'
    print()
    print('Welcome to Distributed Bank!')
    print("------------------------------------------------------")
    print("* Enter you operation:                *")
    print("*    1: Look up balance               *")
    print("*    2: Withdraw an amount of money   *")
    print("*    3: Save an amount of money       *")
    print("*    4: Terminating program           *")
    print("------------------------------------------------------\n")
    op = input("Your choice: ")
    if op == "1":
      try:
        lookup_balance(stub)
      except:
        if primary == 's1':
          primary = 's2'
        else:
          primary = 's1'
        lookup_balance(stub)
    elif op == "2":
      try:
        withdrawal(stub)
      except:
        if primary == 's1':
          primary = 's2'
        else:
          primary = 's1'
          withdrawal(stub)
    elif op == "3":
      try:
        deposit(stub)
      except:
        if primary == 's1':
          primary = 's2'
        else:
          primary = 's1'
        deposit(stub)
    else:
      sys.exit()
    time.sleep(3)
    # for windows :
    os.system('cls')
    # for linux:
    os.system('clear')

    #response = stub.GetResult(ClientRequest_pb2.ClientRequest(actionType=username))
    #print("Greeter client received: " + str(response.responseAmt))

if __name__ == '__main__':
  run()
