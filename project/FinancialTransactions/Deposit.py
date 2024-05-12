
# Deposit.py
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import pyqtSignal, Qt
import pyodbc  # Add import statement for pyodbc


class DepositWidget(QWidget):
    go_back = pyqtSignal()
    deposit_made = pyqtSignal(str, float)

    def __init__(self, account_manager=None, account_number = None):
        
        super().__init__()

        self.setWindowTitle("Deposit")
        self.setGeometry(100, 100, 400, 300)

        self.account_manager = account_manager  # Setting the account_manager attribute
        self.account_number  = account_number
        self.account_number_label = QLabel("Account Number:")
        self.account_number_input = QLineEdit()
        self.account_number_input.setText(self.account_number)
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()

        self.deposit_button = QPushButton("Make Deposit")
        self.back_button = QPushButton("Back to Home")

        self.deposit_button.clicked.connect(self.make_deposit)
        self.back_button.clicked.connect(self.go_back_to_main_menu)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Make a Deposit</h2>"))
        layout.addWidget(self.account_number_label)
        layout.addWidget(self.account_number_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.deposit_button)
        layout.addWidget(self.back_button)
        layout.setAlignment(Qt.AlignCenter)

        self.setStyleSheet(
            "background-color: #f0f0f0;"
            "QLabel { color: #0040ff; }"
            "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px; padding: 10px;}"
            "QPushButton:hover { background-color: #45a049; }"
            "QPushButton:pressed { background-color: #367d3a; }"
        )

        self.setLayout(layout)

    def make_deposit(self):
        account_number = self.account_number_input.text()
        amount = self.amount_input.text()

        if not account_number or not amount:
            QMessageBox.critical(
                self,
                "Error",
                "Please fill in all the fields!",
            )
            return
        try:
            amount = float(amount)
            
        except ValueError:
            QMessageBox.critical(
                self,
                "Error",
                "pleace enter a valid amount!",
            )
            return    
        if not self.account_manager:  # Check if account_manager is provided
            QMessageBox.critical(
                self,
                "Error",
                "Account manager not provided!",
            )
            return

        try:
                
            from_account_balance = self.account_manager.get_balance(account_number)
            if from_account_balance is None:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Account not found",
                )
                return
            # if amount > from_account_balance:
            #     QMessageBox.critical(
            #         self,
            #         "Error",
            #         "Insufficient balance for the deposit.",
            #     )
            #     return
            # Call deposit method from AccountManager
            self.account_manager.deposit(account_number, amount)
            QMessageBox.information(self, "Success", f"Deposit of {amount} made successfully to account {account_number}.")
            self.deposit_made.emit(account_number, amount)
            self.account_number_input.clear()
            self.amount_input.clear()
            #history
            # self.account_manager.deposit(account_number, amount)
            self.account_manager.record_transaction(account_number, "Deposit", amount)  # Record transaction
        except pyodbc.Error as e:
            error_message = str(e).replace("\n", " ")
            QMessageBox.critical(
                self,
                "Error",
                f"Database Error: {error_message}\nPlease ensure the server and database are correctly configured!",
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"An unexpected error occurred: {str(e)}",
            )

    def go_back_to_main_menu(self):
        self.go_back.emit()
        self.close()
