# connection.py
# import mysql.connector

import pyodbc
class AccountManager:
    def __init__(self, server, database, username=None, password=None):
        if username is None and password is None:
            self.connection = pyodbc.connect(
                driver="{SQL Server}",
                server=server,
                database=database,
                Trusted_Connection="yes",  # Use Windows Authentication
            )
        else:
            self.connection = pyodbc.connect(
                driver="{SQL Server}",
                server=server,
                database=database,
                uid=username,
                pwd=password,
            )
        self.cursor = self.connection.cursor()

    def create_account(self, account_number, account_type, name, father_name, address, mobile_number, email, password, balance,mac_address):
        query = "INSERT INTO account (Name, FatherName, Address, MobileNumber, Email, Password, AccountNumber, AccountType, Balance,MAC_Address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,?)"
        values = (name, father_name, address, mobile_number, email, password, account_number, account_type, balance,mac_address)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Account created successfully.")

    def get_account(self, account_number):
        query = "SELECT * FROM account WHERE AccountNumber = ?"
        self.cursor.execute(query, (account_number,))
        return self.cursor.fetchone()
    def get_balance(self,account_number):
        query = "SELECT Balance FROM account WHERE AccountNumber = ?"
        self.cursor.execute(query, (account_number,))
        result =  self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
    def update_account(self, account_number, new_account_type,email, mobile_number, password):
        query = "UPDATE account SET AccountType = ? , MobileNumber = ?,Email = ? , Password = ? WHERE AccountNumber = ?"
        values = (new_account_type, email, mobile_number, password, account_number)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Account updated successfully.")

    def delete_account(self, account_number):
        query = "DELETE FROM account WHERE AccountNumber = ?"
        self.cursor.execute(query, (account_number,))
        self.connection.commit()
        print("Account deleted successfully.")

    def deposit(self, account_number, amount):
        query = "UPDATE account SET Balance = Balance + ? WHERE AccountNumber = ?"
        values = (amount, account_number)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Deposit successful.")

    def withdraw(self, account_number, amount):
        query = "UPDATE account SET Balance = Balance - ? WHERE AccountNumber = ?"
        values = (amount, account_number)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Withdrawal successful.")

    def transfer(self, from_account, to_account, amount):
        self.withdraw(from_account, amount)
        self.deposit(to_account, amount)
        print("Transfer successful.")

    def get_account_info(self, account_number):
        query = "SELECT * FROM account WHERE AccountNumber = ?"
        self.cursor.execute(query, (account_number,))
        return self.cursor.fetchone()
    
    def record_transaction(self, account_number, transaction_type, amount):
        query = "INSERT INTO transaction_history (account_number, transaction_type, amount, timestamp) VALUES (?, ?, ?, GETDATE())"
        values = (account_number, transaction_type, amount)
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Transaction recorded successfully.")
        
    def request_service(self, account_number, service_type):
        # Implement service request logic here
        pass

    def manage_recurring_payments(self, account_number, payment_details):
        # Implement recurring payment management logic here
        pass

    def authenticate_user(self, username, password):
        query = "SELECT * FROM users WHERE username = ? AND password = ?"
        self.cursor.execute(query, (username, password))
        user = self.cursor.fetchone()
        if user:
            print("Authentication successful.")
            return True
        else:
            print("Authentication failed.")
            return False

    def encrypt_data(self, data):
        # Implement data encryption logic here
        pass

    def comply_regulations(self):
        # Implement compliance with regulations logic here
        pass

    def close_connection(self):
        self.cursor.close()
        self.connection.close()
   