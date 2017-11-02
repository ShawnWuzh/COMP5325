import sys


def lookup_balance():
    acct_id = input("Enter your account ID:")
    print("implement the lookup balance code")

def withdrawal():
    acct_id = input("Enter your account ID:")
    amt = input("Enter amount your want to withdraw:")
    print("implement the withdraw code")

def deposite():
    acct_id = input("Enter your account ID:")
    amt = input("Enter amount your want to deposite:")
    print("implement the deposite code")

if __name__ == "__main__":
    while(True):
        op = input("Enter you operation:\
        \n1: Look up balance\
        \n2: Withdraw an amount of money\
        \n3: Save an amount of money\
        \n4: Terminating program\n")
        if op == 1:
            lookup_balance()
        elif op == 2:
            withdrawal();
        elif op == 3:
            deposite()
        else:
            sys.exit()
