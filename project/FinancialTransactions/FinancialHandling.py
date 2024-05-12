
#FinancialHandling.py
import sys
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QMessageBox,
    QApplication,
)
from PyQt5.QtCore import Qt, pyqtSignal
import pyodbc
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QTransform, QIcon
from AccountManagement.AccountHandling import AccountWindow
from connection import AccountManager
from FinancialTransactions.Deposit import DepositWidget
from FinancialTransactions.Transfer import TransferWidget
from FinancialTransactions.Withdraw import WithdrawWidget
from FinancialTransactions.History import TransactionHistoryWidget

class FinancialWidget(QWidget):
    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Financial Menue")
        self.setGeometry(100, 100, 400, 300)

        self.button_layout = QGridLayout()

        self.deposit_button = QPushButton("Deposit Money", self)
        self.deposit_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #3e8e41; }"
                                      "QPushButton:pressed { background-color: #2e7d32; }")

        self.button_layout.addWidget(self.deposit_button, 0, 0, 1, 2)

        self.transfer_button = QPushButton("Transfer Money", self)
        self.transfer_button.setStyleSheet("QPushButton { background-color: #00bcd4; color: white; font-size: 14px; }"
                                        "QPushButton:hover { background-color: #0097a7; }"
                                        "QPushButton:pressed { background-color: #00838f; }")

        self.button_layout.addWidget(self.transfer_button, 1, 0, 1, 2)

        self.withdraw_button = QPushButton("Withdraw Money", self)
        self.withdraw_button.setStyleSheet("QPushButton { background-color: #009688; color: white; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #00796b; }"
                                      "QPushButton:pressed { background-color: #00695c; }")

        self.button_layout.addWidget(self.withdraw_button, 2, 0, 1, 2)
        
        self.history_button = QPushButton("History", self)
        self.history_button.setStyleSheet("QPushButton { background-color: #009688; color: white; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #00796b; }"
                                      "QPushButton:pressed { background-color: #00695c; }")

        self.button_layout.addWidget(self.history_button, 3, 0, 1, 2)
        
        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet("QPushButton {"
            "   background-color: #f44336;"  # Red background color
            "   color: white;"                # White text color
            "   font-size: 14px;"             # Font size
            "   padding: 10px 20px;"          # Padding (top/bottom, left/right)
            "}"
            "QPushButton:hover {"
            "   background-color: #e53935;"   # Darker red background color on hover
            "}"
            "QPushButton:pressed {"
            "   background-color: #d32f2f;"   # Even darker red background color when pressed
            "}")
        
        self.button_layout.addWidget(self.back_button, 4, 0, 1, 1)
        
        spacer = QLabel("", self)
        self.button_layout.addWidget(spacer, 4, 1, 1, 1)
        
        self.setLayout(self.button_layout)
        self.history_label = QLabel("<h2>Transaction History</h2>")
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)  
        self.history_table.setHorizontalHeaderLabels(["Transaction ID", "Account Number", "Transaction Type", "Amount", "Date"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.account_manager = AccountManager(server=r"NAMASTE\SQLEXPRESS", database="BankSystem")
        self.deposit_widget = DepositWidget(self.account_manager)
        self.deposit_widget.go_back.connect(self.show)  # Connect the signal to a slot that shows FinancialWidget
        self.transfer_widget = TransferWidget(self.account_manager)
        self.transfer_widget.go_back.connect(self.show)
        self.withdraw_Widget = WithdrawWidget(self.account_manager)
        self.withdraw_Widget.go_back.connect(self.show)
        self.history_widget = TransactionHistoryWidget(self.account_manager)
        self.history_widget.go_back.connect(self.show)
        font = QFont("Arial", 14)
        self.deposit_button.setFont(font)
        self.transfer_button.setFont(font)
        self.withdraw_button.setFont(font)
        self.back_button.setFont(font)
        layout = QVBoxLayout()
        layout.addWidget(self.history_label)
        
        layout.addWidget(self.history_table)
        pixmap = QPixmap("back_icon.png")
        transform = QTransform()
        back_icon = QIcon(pixmap.transformed(transform))
        self.back_button.setIcon(back_icon)
        self.back_button.clicked.connect(self.go_back_to_main_menu)
        self.deposit_button.clicked.connect(self.show_transfer_formD)
        self.transfer_button.clicked.connect(self.show_transfer_form)
        self.withdraw_button.clicked.connect(self.show_transfer_formW)
        self.history_button.clicked.connect(self.show_history_form)
        self.history_button.clicked.connect(lambda:self.load_history(None))
        
    def show_deposit_form(self):
        self.deposit_widget.show()
        self.close()    
    def show_transfer_form(self):
        try:
            # Connect to the database
            connection = pyodbc.connect(
                driver="{SQL Server}",
                server=r"NAMASTE\SQLEXPRESS",
                database="BankSystem",
                trusted_connection="yes",
            )

            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # Execute a query to retrieve the last logged-in account number from login_log table
            cursor.execute("SELECT TOP 1 account_number FROM login_log ORDER BY login_time DESC")
            row = cursor.fetchone()

            # Check if a row was returned
            if row:
                from_account = row[0]
                print("Successfully retrieved from_account:", from_account)  # Debug print statement

                # Show the transfer form with the retrieved account number
                self.transfer_widget = TransferWidget(self.account_manager, from_account)  # Pass both arguments
                print("From Account in homepage.py:", from_account) 
                self.transfer_widget.go_back.connect(self.show)  # Connect the signal to a slot that shows FinancialWidget
                self.transfer_widget.show()
            else:
                QMessageBox.warning(self, "Warning", "No login history found.")
            
            # Close the cursor and connection
            cursor.close()
            connection.close()
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Error", f"Error retrieving login history: {e}")

    def show_withdraw_form(self):
        self.withdraw_Widget.show()
        self.close()  
    def show_history_form(self):
        # Retrieve account number from the login_log table
        try:
            # Connect to the database
            connection = pyodbc.connect(
                driver="{SQL Server}",
                server=r"NAMASTE\SQLEXPRESS",
                database="BankSystem",
                trusted_connection="yes",
            )

            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # Execute a query to retrieve the last logged-in account number from login_log table
            cursor.execute("SELECT TOP 1 account_number FROM login_log ORDER BY login_time DESC")
            row = cursor.fetchone()

            # Check if a row was returned
            if row:
                account_number = row[0]

                # Show the history for the retrieved account number
                print("Account Number History:", account_number)
                self.history_widget.show()
                self.history_widget.load_history(account_number)
            else:
                QMessageBox.warning(self, "Warning", "No login history found.")
            
            # Close the cursor and connection
            cursor.close()
            connection.close()
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Error", f"Error retrieving login history: {e}")
    
    def show_transfer_formD(self):
        try:
            # Connect to the database
            connection = pyodbc.connect(
                driver="{SQL Server}",
                server=r"NAMASTE\SQLEXPRESS",
                database="BankSystem",
                trusted_connection="yes",
            )

            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # Execute a query to retrieve the last logged-in account number from login_log table
            cursor.execute("SELECT TOP 1 account_number FROM login_log ORDER BY login_time DESC")
            row = cursor.fetchone()

            # Check if a row was returned
            if row:
                account_number = row[0]
                print("Successfully retrieved from_account:", account_number)  # Debug print statement

                # Show the transfer form with the retrieved account number
                self.transfer_widget = DepositWidget(self.account_manager, account_number)  # Pass both arguments
                print("From Account in homepage.py:", account_number) 
                self.transfer_widget.go_back.connect(self.show)  # Connect the signal to a slot that shows FinancialWidget
                self.transfer_widget.show()
            else:
                QMessageBox.warning(self, "Warning", "No login history found.")
            
            # Close the cursor and connection
            cursor.close()
            connection.close()
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Error", f"Error retrieving login history: {e}")

    
    # def go_back_to_main_menu(self):
    #     self.go_back.emit()
    #     self.close()
    def load_history(self,account_number):
        # account_numberf = self.account_number
        if not account_number:
            return

        try:
            query = "SELECT transaction_id, account_number, transaction_type, amount, CONVERT(varchar, timestamp, 20) FROM transaction_history WHERE account_number = ?"
            self.account_manager.cursor.execute(query, (account_number,))
            history = self.account_manager.cursor.fetchall()
            self.history_table.setRowCount(len(history))
            for row_idx, row in enumerate(history):
                for col_idx, data in enumerate(row):
                    item = QTableWidgetItem(str(data))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.history_table.setItem(row_idx, col_idx, item)
        except pyodbc.Error as e:
            print("Error fetching transaction history:", e)
    
    
    def show_transfer_formW(self):
        try:
            # Connect to the database
            connection = pyodbc.connect(
                driver="{SQL Server}",
                server=r"NAMASTE\SQLEXPRESS",
                database="BankSystem",
                trusted_connection="yes",
            )

            # Create a cursor to execute SQL queries
            cursor = connection.cursor()

            # Execute a query to retrieve the last logged-in account number from login_log table
            cursor.execute("SELECT TOP 1 account_number FROM login_log ORDER BY login_time DESC")
            row = cursor.fetchone()

            # Check if a row was returned
            if row:
                account_number = row[0]
                print("Successfully retrieved from_account:", account_number)  # Debug print statement

                # Show the transfer form with the retrieved account number
                self.transfer_widget = WithdrawWidget(self.account_manager, account_number)  # Pass both arguments
                print("From Account in homepage.py:", account_number) 
                self.transfer_widget.go_back.connect(self.show)  # Connect the signal to a slot that shows FinancialWidget
                self.transfer_widget.show()
            else:
                QMessageBox.warning(self, "Warning", "No login history found.")
            
            # Close the cursor and connection
            cursor.close()
            connection.close()
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Error", f"Error retrieving login history: {e}")

    
    
    def go_back_to_main_menu(self):
        self.go_back.emit()
        self.close()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinancialWidget()
    window.show()
    sys.exit(app.exec_())
