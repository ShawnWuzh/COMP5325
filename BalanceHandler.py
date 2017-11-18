import json
from threading import Lock
from GlobVar import Globvar


class BalanceHandler(object):
    FILE_LOCK = Lock()

    def __init__(self):
        self.acc_id = None
        self.balance_dict = None
        self.load_balance_data()

    def load_balance_data(self):
        with open('./balance.json') as json_data:
            self.balance_dict = json.load(json_data)

    def lookup_balance(self, key):
        with BalanceHandler.FILE_LOCK:
            self.acc_id = None
            if key in self.balance_dict.keys():
                self.acc_id = key
                return self.balance_dict[key]
            else:
                return "Account not found"

    def deposit(self, amt):
        with BalanceHandler.FILE_LOCK:
            if self.acc_id == None:
                return "Account not found"
            if amt <= 0:
                return "Desposite amount must be greater than 0"
            current_amount = self.balance_dict[self.acc_id]
            self.balance_dict[self.acc_id] = current_amount + amt
            self.export_to_file()
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
                self.export_to_file()
                return "SUCCESS"

    def synchronize(self, dict):
        with BalanceHandler.FILE_LOCK:
            self.balance_dict = dict
            self.export_to_file()

    def export_to_file(self):
        with open('balance.json', 'w') as outfile:
            json.dump(self.balance_dict, outfile)

    def serialization(self):
        serialized_data = json.dumps(self.balance_dict) + Globvar.ACTION_ID
        return serialized_data