import json
from threading import Lock


class BalanceHandler(object):
    FILE_LOCK = Lock()

    def __init__(self):
        self.acc_id = None
        with open('./balance.json') as json_data:
            self.balance_dict = json.load(json_data)

    def lookup_balanace(self, key):
        self.acc_id = None
        if key in self.balance_dict.keys():
            self.acc_id = key
            return self.balance_dict[key]
        else:
            return "Account not found"

    def deposite(self, amt):
        with BalanceHandler.FILE_LOCK:
            if self.acc_id == None:
                return "Account not found"
            if amt <= 0:
                return "Desposite amount must be greater than 0"
            current_amount = self.balance_dict[self.acc_id]
            self.balance_dict[self.acc_id] = current_amount + amt
            self.__export()
            return "SUCCESS"

    def withdraw(self, amt):
        with BalanceHandler.FILE_LOCK:
            if self.acc_id == None:
                return "Account not found"
            elif amt <= 0:
                return "Desposite amount must be greater than 0"
            elif self.balance_dict[self.acc_id] < amt:
                return "Desposite amount must be less than balance"
            else:
                current_amount = self.balance_dict[self.acc_id]
                self.balance_dict[self.acc_id] = current_amount - amt
                self.__export()
                return "SUCCESS"

    def synchronize(self, dict):
        with BalanceHandler.FILE_LOCK:
            self.balance_dict = dict
            self.__export()

    def __export(self):
        with open('balance.json', 'w') as outfile:
            json.dump(self.balance_dict, outfile)