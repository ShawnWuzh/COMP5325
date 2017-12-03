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

from GlobVar import  Globvar
import grpc
import sys
import time
import os
import ClientRequest_pb2
import ClientRequest_pb2_grpc

global_var = Globvar()
def lookup_balance(stub,acct_id):
  try:
    while(True):
      response = stub.GetBalance(ClientRequest_pb2.ClientRequest(acctId=acct_id,actionId=global_var.ACTION_ID))
      if response.status == 'SUCCESS':
        print("Current balance: " + str(response.responseAmt)+ "\n\n")
        global_var.ACTION_ID = response.actionId
        break
      elif response.status == 'REJECT':
        continue
      else:
        print(response.status)
        break
    return True
  except:
    return False



def withdrawal(stub,acct_id,amt):
  try:
    while(True):
      response = stub.Withdraw(ClientRequest_pb2.ClientRequest(acctId=acct_id,requestAmt=int(amt),actionId=global_var.ACTION_ID))
      if response.status == 'SUCCESS':
        print("Current balance: " + str(response.responseAmt) + "\n\n")
        global_var.ACTION_ID = response.actionId
        break
      elif response.status == 'REJECT':
        continue
      else:
        print(response.status)
        break
    return True
  except:
    return False


def deposit(stub,acct_id,amt):
  try:
    while(True):
      response = stub.Deposit(ClientRequest_pb2.ClientRequest(acctId=acct_id,requestAmt=int(amt),actionId=global_var.ACTION_ID))
      if response.status == 'SUCCESS':
        print("Current balance: " + str(response.responseAmt)+ "\n\n")
        global_var.ACTION_ID = response.actionId

        break
      elif response.status == 'REJECT':
        print('Reject!')
        continue
      else:
        print(response.status)
        break
    return True
  except:
    return False


def run():
  with open('./serverhost.config') as sever_data:
    addr_list = json.load(sever_data)
  primary = 's1'
  try:
    channel = grpc.insecure_channel('{}:50051'.format(addr_list[primary]))
    stub = ClientRequest_pb2_grpc.GreeterStub(channel)
  except:
    if primary == 's1':
      primary = 's2'
    else:
      primary = 's1'
    channel = grpc.insecure_channel('{}:50051'.format(addr_list[primary]))
    stub = ClientRequest_pb2_grpc.GreeterStub(channel)
  while (True):
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
      acct_id = input("Enter your account ID: ")
      while(not lookup_balance(stub,acct_id)):
        if primary == 's1':
          primary = 's2'
        else:
          primary = 's1'
        channel = grpc.insecure_channel('{}:50051'.format(addr_list[primary]))
        stub = ClientRequest_pb2_grpc.GreeterStub(channel)
    elif op == "2":
      acct_id = input("Enter your account ID: ")
      amt = input("Enter amount your want to withdraw: ")
      while(not withdrawal(stub,acct_id,amt)):
        if primary == 's1':
          primary = 's2'
        else:
          primary = 's1'
        channel = grpc.insecure_channel('{}:50051'.format(addr_list[primary]))
        stub = ClientRequest_pb2_grpc.GreeterStub(channel)
    elif op == "3":
      acct_id = input("Enter your account ID: ")
      amt = input("Enter amount your want to deposite: ")
      while(not deposit(stub,acct_id,amt)):
        if primary == 's1':
          primary = 's2'
        else:
          primary = 's1'
        channel = grpc.insecure_channel('{}:50051'.format(addr_list[primary]))
        stub = ClientRequest_pb2_grpc.GreeterStub(channel)
    else:
      sys.exit()
    time.sleep(3)
    # for windows :
    # os.system('cls')
    # for linux:
    os.system('clear')

    #response = stub.GetResult(ClientRequest_pb2.ClientRequest(actionType=username))
    #print("Greeter client received: " + str(response.responseAmt))

if __name__ == '__main__':
  run()
