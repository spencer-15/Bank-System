#Withdraw.py
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtCore import pyqtSignal, Qt
import pyodbc

class WithdrawWidget(QWidget):
    go_back = pyqtSignal()
    money_withdrawn = pyqtSignal(str, float)

    def __init__(self, account_manager,account_number = None):
        super().__init__()

        self.setWindowTitle("Withdraw Money")
        self.setGeometry(100, 100, 400, 300)

        self.account_manager = account_manager
        self.account_number  = account_number
        
        self.account_number_label = QLabel("Account Number:")
        self.account_number_input = QLineEdit()
        self.account_number_input.setText(self.account_number)
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()

        self.withdraw_button = QPushButton("Withdraw Money")
        self.back_button = QPushButton("Back to Home")

        self.withdraw_button.clicked.connect(self.withdraw)
        self.back_button.clicked.connect(self.go_back_to_main_menu)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Withdraw Money</h2>"))
        layout.addWidget(self.account_number_label)
        layout.addWidget(self.account_number_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.withdraw_button)
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

    def withdraw(self):
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
                "Error",
                "Invalid amount pleace enter amount to withdrawl ",
            )    
            return
        try:
            balance = self.account_manager.get_balance(account_number)
            if balance is None:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Account not found"
                )
                return
            if amount > balance:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Insufficient Balance"
                )
                return
            
            QMessageBox.information(
                self, 
                "Success", 
                f"Successfully withdrawn {amount} from account {account_number}."
            )
            self.money_withdrawn.emit(account_number, amount)
            self.account_number_input.clear()
            self.amount_input.clear()
            #transiction History
            self.account_manager.withdraw(account_number, amount)
            self.account_manager.record_transaction(account_number, "Withdraw", amount)  # Record withdrawal transaction
        except pyodbc.Error as e:
            error_message = str(e).replace("\n", " ")
            QMessageBox.critical(
                self, 
                "Error",
                f"Database Error: {error_message}\nPlease ensure the server and database are correctly configured!",
            )

    def go_back_to_main_menu(self):
        self.go_back.emit()
        self.close()
