#Delete.py
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import pyodbc


class DeleteAccountWidget(QWidget):
    account_deleted = pyqtSignal(str)
    go_back = pyqtSignal()

    def __init__(self, account_manager,account_number = None):
        super().__init__()

        self.setWindowTitle("Delete Account")
        self.setGeometry(100, 100, 400, 300)

        self.account_manager = account_manager
        self.account_number =account_number
        self.account_number_label = QLabel("Account Number:")
        self.account_number_input = QLineEdit()
        self.account_number_input.setText(self.account_number)
        self.delete_account_button = QPushButton("Delete Account")
        self.back_button = QPushButton("Back to Home")
        self.delete_account_button.clicked.connect(self.delete_account)
        self.back_button.clicked.connect(self.go_back_to_main_menu)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Delete Account</h2>"))
        layout.addWidget(self.account_number_label)
        layout.addWidget(self.account_number_input)
        layout.addWidget(self.delete_account_button)
        layout.addWidget(self.back_button)
        layout.setAlignment(Qt.AlignCenter)

        self.setStyleSheet(
            "background-color: #f0f0f0;"
            "QLabel { color: #ff0000; }"
            "QPushButton { background-color: #f44336; color: white; font-weight: bold; border-radius: 5px; padding: 10px;}"
            "QPushButton:hover { background-color: #e53935; }"
            "QPushButton:pressed { background-color: #d32f2f; }"
        )

        self.setLayout(layout)

    def delete_account(self):
        account_number = self.account_number_input.text()

        if not account_number:
            QMessageBox.critical(
                self,
                "Error",
                "Please fill in the Account Number field!",
            )
            return

        try:
            account = self.account_manager.get_account(account_number)
            if account:
                self.account_manager.delete_account(account_number)
                QMessageBox.information(self, "Success", "Account deleted successfully.")
                self.account_deleted.emit(account_number)
                self.account_number_input.clear()  # Clear the input area
                self.close()
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Account not found in the database!",
                )
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
