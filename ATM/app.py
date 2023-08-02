import os
import threading
import time

class ATM:
    def __init__(self):
        self.atm_balance = {}
        self.customers = {}
        self.load_atm_balance()
        self.load_customer_details()

    
   


    def load_atm_balance(self):
        if os.path.exists("atm_balance.txt"):
            with open("atm_balance.txt", "r") as file:
                for line in file:
                    denomination, count, value = line.strip().split()
                    self.atm_balance[int(denomination)] = {
                        "count": int(count),
                        "value": int(value),
                    }
        else:
            self.atm_balance = {2000: {"count": 0, "value": 0},
                                500: {"count": 0, "value": 0},
                                100: {"count": 0, "value": 0}}

    def load_customer_details(self):
        if os.path.exists("customer_details.txt"):
            with open("customer_details.txt", "r") as file:
                for line in file:
                    acc_no, account_holder, pin, balance = line.strip().split()
                    self.customers[int(acc_no)] = {
                        "account_holder": account_holder,
                        "pin": int(pin),
                        "balance": int(balance),
                    }

    def save_atm_balance(self):
        with open("atm_balance.txt", "w") as file:
            for denomination, data in self.atm_balance.items():
                file.write(f"{denomination} {data['count']} {data['value']}\n")

    def save_customer_details(self):
        with open("customer_details.txt", "w") as file:
            for acc_no, data in self.customers.items():
                file.write(f"{acc_no} {data['account_holder']} {data['pin']} {data['balance']}\n")

    def show_atm_balance(self):
        print("Denomination\tNumber\tValue")
        total_amount = 0
        for denomination, data in self.atm_balance.items():
            total_amount += data['value']
            print(f"{denomination}\t{data['count']}\t{data['value']}")
        print(f"\nTotal Amount available in the ATM = {total_amount} ₹")

    def show_customer_details(self):
        print("Acc No\tAccount Holder\tPin Number\tAccount Balance")
        for acc_no, data in self.customers.items():
            print(f"{acc_no}\t{data['account_holder']}\t{data['pin']}\t{data['balance']} ₹")

    def handle_atm_process(self):
        acc_no = int(input("Enter Account Number: "))
        pin = int(input("Enter PIN Number: "))

        if acc_no in self.customers and self.customers[acc_no]['pin'] == pin:
            print("\nWelcome to ATM Services!")
            while True:
                print("\n1. Check Balance")
                print("2. Withdraw Money")
                print("3. Transfer Money")
                print("4. Check ATM Balance")
                print("5. Mini Statement")
                print("6. Exit")
                option = int(input("Enter your choice: "))

                if option == 1:
                    self.check_balance(acc_no)
                elif option == 2:
                    self.withdraw_money(acc_no)
                elif option == 3:
                    self.transfer_money(acc_no)
                elif option == 4:
                    self.show_atm_balance()
                elif option == 5:
                    self.show_mini_statement(acc_no)
                elif option == 6:
                    print("\nThank you for using ATM services!")
                    break
                else:
                    print("\nInvalid option! Please try again.")

        else:
            print("\nInvalid Account Number or PIN!")

    def check_balance(self, acc_no):
        print(f"\nAccount Balance for {self.customers[acc_no]['account_holder']} = {self.customers[acc_no]['balance']} ₹")

    def withdraw_money(self, acc_no):
        amount = int(input("\nEnter the amount to be withdrawn: "))

        if 100 <= amount <= 10000 and amount <= self.customers[acc_no]['balance']:
            denominations = [2000, 500, 100]
            notes = {denom: 0 for denom in denominations}
            temp_amount = amount

            for denom in denominations:
                while temp_amount >= denom and self.atm_balance[denom]['count'] > 0:
                    temp_amount -= denom
                    self.atm_balance[denom]['count'] -= 1
                    notes[denom] += 1

            if temp_amount == 0:
                self.customers[acc_no]['balance'] -= amount
                self.save_atm_balance()
                self.save_customer_details()
                print("\nTransaction successful! Please collect your cash.")
                print("Dispensed denominations:")
                for denom, count in notes.items():
                    if count > 0:
                        print(f"{denom}₹ X {count}")

            else:
                print("\nATM does not have sufficient denominations to vend.")

        else:
            print("\nInvalid amount or insufficient balance.")

    def transfer_money(self, sender_acc_no):
        amount = int(input("\nEnter the amount to be transferred: "))
        if 1000 <= amount <= 10000 and amount <= self.customers[sender_acc_no]['balance']:
            receiver_acc_no = int(input("Enter the recipient's Account Number: "))

            if receiver_acc_no in self.customers and receiver_acc_no != sender_acc_no:
                self.customers[sender_acc_no]['balance'] -= amount
                self.customers[receiver_acc_no]['balance'] += amount
                self.save_customer_details()
                print("\nMoney transferred successfully!")

            else:
                print("\nInvalid recipient's Account Number.")

        else:
            print("\nInvalid amount or insufficient balance.")

   
       

 

    def show_mini_statement(self, acc_no):
        file_name = f"{acc_no}_transactions.txt"
        if not os.path.exists(file_name):
            print("\nNo transaction history available.")
            return

        with open(file_name, "r") as file:
            lines = file.readlines()

        transactions = []
        for line in lines:
            transaction_no, _, _, _, _ = line.strip().split("\t")
            transactions.append((int(transaction_no), line.strip()))

        transactions = sorted(transactions, key=lambda x: x[0], reverse=True)

        print("\nMini Statement:")
        print("Transaction Number\tDescription\tCredit / Debit\tAmount\tClosing Balance")
        for _, transaction in transactions[:10]:
            print(transaction)

 



    def log_transaction(self, acc_no, description, credit_debit, amount, closing_balance):
        file_name = f"{acc_no}_transactions.txt"
        with open(file_name, "a") as file:
            file.write(f"{self.get_next_transaction_number(acc_no)}\t{description}\t{credit_debit}\t{amount}\t{closing_balance}\n")

    def get_next_transaction_number(self, acc_no):
        file_name = f"{acc_no}_transactions.txt"
        if not os.path.exists(file_name):
            return 1001

        with open(file_name, "r") as file:
            lines = file.readlines()
            if lines:
                last_transaction_number = int(lines[-1].split("\t")[0])
                return last_transaction_number + 1
            else:
                return 1001



   
    def create_customer_details_file(self):
        with open("customer_details.txt", "w") as file:
            file.write("101 Suresh 2343 25234\n")
            file.write("102 Ganesh 5432 34123\n")
            file.write("103 Magesh 7854 26100\n")
            file.write("104 Naresh 2345 80000\n")
            file.write("105 Harish 1907 103400\n")        

# Main Program
if __name__ == "__main__":
    atm = ATM()
    
    
    atm.create_customer_details_file()
    
    while True:
        print("\nMain Menu:")
        print("1. Load Cash to ATM")
        print("2. Show Customer Details")
        print("3. Show ATM Operations")
        print("4. Exit")
        option = int(input("Enter your choice: "))

        if option == 1:
            atm.show_atm_balance()
            denominations = [2000, 500, 100]
            for denom in denominations:
                count = int(input(f"Enter the number of {denom}₹ notes to load: "))
                value = count * denom
                atm.atm_balance[denom]['count'] += count
                atm.atm_balance[denom]['value'] += value
            atm.save_atm_balance()

        elif option == 2:
            atm.show_customer_details()

        elif option == 3:
            atm.handle_atm_process()

        elif option == 4:
            print("\nThank you for using the ATM. Have a nice day!")
            break

        else:
            print("\nInvalid option! Please try again.")
