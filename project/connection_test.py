import unittest
from unittest.mock import MagicMock
from connection import AccountManager

class TestAccountManager(unittest.TestCase):

    def setUp(self):
        # Mocking pyodbc connection and cursor
        self.mock_connection = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_connection.cursor.return_value = self.mock_cursor

        # Creating an instance of AccountManager with mocked connection
        self.account_manager = AccountManager(server="DESKTOP-K8BIO91\SQLEXPRESS", database="BankSystem")
        self.account_manager.connection = self.mock_connection

    # def test_create_account(self):
    #     # Mocking execute and commit methods
    #     self.mock_cursor.execute = MagicMock()
    #     self.mock_connection.commit = MagicMock()

    #     # Test data
    #     account_number = "ulp55121167865161"
    #     account_type = "Personal"
    #     name = "alex"
    #     father_name = "asd"
    #     address = "ads"
    #     mobile_number = "1222222222222"
    #     email = "janidali957@gmail.com"
    #     password = "Alex123#"
    #     balance = 1000.0
    #     mac_address = "38-F3-AB-31-B7-E1"

    #     # Calling the method to test
    #     # self.account_manager.create_account(account_number, account_type, name, father_name, address, mobile_number, email, password, balance, mac_address)

    #     # Asserting that execute and commit methods were called with correct arguments
    #     # # self.mock_cursor.execute.assert_called_once_with(
    #     #     "INSERT INTO account (Name, FatherName, Address, MobileNumber, Email, Password, AccountNumber, AccountType, Balance, MAC_Address) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #     #     (name, father_name, address, mobile_number, email, password, account_number, account_type, balance, mac_address)
    #     # )
    #     # self.mock_connection.commit.assert_called_once()

    # Add more test methods for other functionalities

if __name__ == '__main__':
    unittest.main()
