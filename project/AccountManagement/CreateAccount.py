


import random
import string
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QCheckBox,
)

import re
from PyQt5.QtCore import pyqtSignal, Qt
import pyodbc
import subprocess
class CreateAccountWidget(QWidget):
    account_created = pyqtSignal(str, str,str,str,str)
    go_back = pyqtSignal()

    def __init__(self, account_manager):
        super().__init__()

        self.setWindowTitle("Create New Account")
        self.setGeometry(100, 100, 400, 300)

        self.account_manager = account_manager

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()

        self.father_name_label = QLabel("Father's Name:")
        self.father_name_input = QLineEdit()

        self.address_label = QLabel("Address:")
        self.address_input = QLineEdit()

        self.mobile_number_label = QLabel("Mobile Number:")
        self.mobile_number_input = QLineEdit()
        
        self.Email_label = QLabel("Email:")
        self.Email_input = QLineEdit()
        
        self.show_password_button = QPushButton("Show Password")
        self.show_password_button.clicked.connect(self.toggle_password_visibility)
        self.show_password_button.setMaximumWidth(95)
        self.Password_label = QLabel("Password:")
        self.Password_input = QLineEdit()
        self.Password_input.setEchoMode(QLineEdit.Password)
        
        self.Confirm_Password_label = QLabel("Confirm Password:")
        self.Confirm_Password_input = QLineEdit()
        self.Confirm_Password_input.setEchoMode(QLineEdit.Password)
        
        self.account_number_label = QLabel("Account Number:")
        self.account_number_input = QLineEdit()

        self.account_type_label = QLabel("Account Type:")
        self.account_type_personal_checkbox = QCheckBox("Personal")
        self.account_type_business_checkbox = QCheckBox("Business")
        
        self.Balance_label = QLabel("Balance :")
        self.Balance_input = QLineEdit()
        self.create_account_button = QPushButton("Create Account")
        self.create_account_button.clicked.connect(self.create_account)
       
        self.back_button = QPushButton("Back to Home")
        self.back_button.clicked.connect(self.go_back_to_main_menu)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Create New Account</h2>"))
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.father_name_label)
        layout.addWidget(self.father_name_input)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)
        layout.addWidget(self.mobile_number_label)
        layout.addWidget(self.mobile_number_input)
        layout.addWidget(self.Email_label)
        layout.addWidget(self.Email_input)
        layout.addWidget(self.Password_label)
        layout.addWidget(self.Password_input)
        layout.addWidget(self.Confirm_Password_label)
        layout.addWidget(self.Confirm_Password_input)
        layout.addWidget(self.show_password_button)
        layout.addWidget(self.Balance_label)
        layout.addWidget(self.Balance_input)
        
        # layout.addWidget(self.account_number_input)
        layout.addWidget(self.account_type_label)
        layout.addWidget(self.account_type_personal_checkbox)
        layout.addWidget(self.account_type_business_checkbox)
        layout.addWidget(self.account_number_label)
        layout.addWidget(self.account_number_input)
        layout.addWidget(self.create_account_button)
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

        self.account_type_personal_checkbox.stateChanged.connect(self.update_account_number)
        self.account_type_business_checkbox.stateChanged.connect(self.update_account_number)

    def generate_account_number(self):
        # Generate a random 14-digit account number
        if self.account_type_personal_checkbox.isChecked():
            self.account_type_business_checkbox.setChecked(False)
            return "ulp"+''.join(random.choices(string.digits, k=14))
        elif self.account_type_business_checkbox.isChecked():
            self.account_type_personal_checkbox.setCheckable(False)
            return "ulb"+''.join(random.choices(string.digits, k=14))
    def update_account_number(self):
        account_type = ""
        if self.account_type_personal_checkbox.isChecked():
            account_type = "Personal"
        elif self.account_type_business_checkbox.isChecked():
            account_type = "Business"

        if account_type:
            self.account_number_input.setText(self.generate_account_number())

    def create_account(self):
        def get_mac_address():
            result = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True)
            output = result.stdout
            lines = output.split("\n")
            for line in lines:
                if "Physical Address" in line:
                    mac_address = line.split(":")[-1].strip()
                    return mac_address
            return None

        mac_address = get_mac_address()
        print("MAC Address:", mac_address)
        name = self.name_input.text()
        father_name = self.father_name_input.text()
        address = self.address_input.text()
        def validate_mobile_number(mobile_number):
            # Regular expression to match a typical mobile number format
            pattern = r'^\d{10,14}$'
            if re.match(pattern, mobile_number):
                return True
            else:
                return False
        mobile_number = self.mobile_number_input.text()
        if not validate_mobile_number(mobile_number):
            QMessageBox.critical(
                self,
                "ERROR",
                "Invalid mobile number format. Please enter a valid mobile number without any spaces or special characters."
            )
            return
        account_number = self.account_number_input.text()
        # Function to validate email format
        def validate_email(email):
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(pattern, email):
                return True
            else:
                return False
        Email = self.Email_input.text()
        # Validate email format
        if not validate_email(Email):
            QMessageBox.critical(
                self,
                "ERROR",
                "Invalid email format. Please enter a valid email address."
            )
            return
        # Function to validate the password 
        def validate_password(password):
            pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*?&]{8,50}$"
            if re.match(pattern, password):
                return True
            else:
                return False

        # Your existing code snippet
        Password = self.Password_input.text()
        Confirm_Password = self.Confirm_Password_input.text()

        # Validate password format
        if not validate_password(Password):
            QMessageBox.critical(
                self,
                "ERROR",
                "Password must contain at least 8 characters, including one uppercase letter, one lowercase letter, one digit, and one special character."
            )
            return

        # Check if Password and Confirm_Password match
        if Password != Confirm_Password:
            QMessageBox.critical(
                self,
                "ERROR",
                "Password and Confirm Password do not match"
            )
            return
        
        Balance = self.Balance_input.text() 
        
        account_type = ""
        if self.account_type_personal_checkbox.isChecked():
            account_type = "Personal"
        elif self.account_type_business_checkbox.isChecked():
            account_type = "Business"

        if not name or not father_name or not address or not mobile_number or not Email or not Password or not Confirm_Password  or not account_type or not Balance:
            QMessageBox.critical(
                self,
                "Error",
                "Please fill in all the fields!",
            )
            return
     
        try:
            self.account_manager.create_account(account_number, account_type, name, father_name, address, mobile_number, Email, Password, Balance,mac_address)
            QMessageBox.information(self, "Success", "Account created successfully.")
            self.name_input.clear()
            self.father_name_input.clear()
            self.Email_input.clear()
            self.mobile_number_input.clear()
            self.Password_input.clear()
            self.Confirm_Password_input.clear()
            self.account_number_input.clear()
            self.account_type_business_checkbox.clearFocus()
            self.account_created.emit(Email, name, Password, account_number, account_type)
            self.go_back.emit()
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
    def toggle_password_visibility(self):
        if self.Password_input.echoMode() == QLineEdit.Password:
            self.Password_input.setEchoMode(QLineEdit.Normal)  # Show plain text
            self.Confirm_Password_input.setEchoMode(QLineEdit.Normal)
            self.show_password_button.setText("Hide Password")
            
        else:
            self.Password_input.setEchoMode(QLineEdit.Password)  # Hide password
            self.Confirm_Password_input.setEchoMode(QLineEdit.Password)  # Hide password
            self.show_password_button.setText("Show Password")
        