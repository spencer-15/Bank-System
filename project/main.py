
import sys

from PyQt5.QtWidgets import QApplication

from gui import AccountManagementApp
from connection import AccountManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Initialize the connection to the database
    server = r"NAMASTE\SQLEXPRESS"  # User name 
    database = "BankSystem"              # database name

    account_manager = AccountManager(server, database)

    bank_system = account_manager

    window = AccountManagementApp(bank_system)

    window.show()

    sys.exit(app.exec())
