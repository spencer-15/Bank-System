#Update.py
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


class UpdateAccountWidget(QWidget):
    account_updated = pyqtSignal(str, str,str,str,str)
    go_back = pyqtSignal()
    def __init__(self, account_manager,account_number = None):
        super().__init__()

        self.setWindowTitle("Update Account")
        self.setGeometry(100, 100, 400, 300)

        self.account_manager = account_manager
        self.account_number = account_number
        self.account_number_label = QLabel("Account Number:")
        self.account_number_input = QLineEdit()
        self.account_number_input.setText(self.account_number)
        self.new_account_type_label = QLabel("New Account Type:")
        self.new_account_type_input = QLineEdit()
        
        self.email_label = QLabel("Email")
        self.email_input = QLineEdit()
        
        self.mobilenumber_label = QLabel("Mobile Number")
        self.mobilenumber_input = QLineEdit()
        
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        
        self.update_account_button = QPushButton("Update Account")
        self.back_button = QPushButton("Back to Home")
        self.update_account_button.clicked.connect(self.update_account)
        self.back_button.clicked.connect(self.go_back_to_main_menu)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Update Account</h2>"))
        layout.addWidget(self.account_number_label)
        layout.addWidget(self.account_number_input)
        
        layout.addWidget(self.new_account_type_label)
        layout.addWidget(self.new_account_type_input)
        
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        
        layout.addWidget(self.mobilenumber_label)
        layout.addWidget(self.mobilenumber_input)
        
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        
        layout.addWidget(self.update_account_button)
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

    def update_account(self):
        account_number = self.account_number_input.text()
        new_account_type = self.new_account_type_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        mobilenumber = self.mobilenumber_input.text()
        if not account_number or not new_account_type or not email or not password or not mobilenumber:
            QMessageBox.critical(
                self,
                "Error",
                "Please fill in all the fields!",
            )
            return

        # if not account_number.isdigit() or len(account_number) != 14:
        #     QMessageBox.critical(
        #         self,
        #         "Error",
        #         "Account Number must be exactly 14 digits!",
        #     )
        #     return
        
        try:
            self.account_manager.update_account(account_number, new_account_type,mobilenumber,email,password)
            QMessageBox.information(self, "Success", "Account updated successfully.")
            self.account_updated.emit(account_number, new_account_type,email,mobilenumber,password)
            self.account_number_input.clear()
            self.new_account_type_input.clear()
            self.email_input.clear()
            self.mobilenumber_input.clear()
            
            self.close()
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
