







from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
import datetime
from PyQt5.QtCore import pyqtSignal, Qt
import pyodbc
import pyotp
import smtplib as s
import hashlib
import base64
import secrets
import sys

class TransferWidget(QWidget):
    go_back = pyqtSignal()
    money_transferred = pyqtSignal(str, str, float)

    def __init__(self, account_manager,from_account=None):
        print("Account Manager:", account_manager)  
        print("From Account:", from_account) 
        super().__init__()
        self.from_account = from_account
        self.setWindowTitle("Transfer Money")
        self.setGeometry(100, 100, 400, 250)

        self.account_manager = account_manager

        self.from_account_label = QLabel("From Account Number:")
        self.from_account_input = QLineEdit()
        self.from_account_input.setText(self.from_account)
        self.to_account_label = QLabel("To Account Number:")
        self.to_account_input = QLineEdit()
        
        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()
      
        self.transfer_button = QPushButton("Transfer Money")
        self.back_button = QPushButton("Back to Home")
        
        self.transfer_button.clicked.connect(self.transfer)
        self.back_button.clicked.connect(self.go_back_to_main_menu)
        self.otp_label = QLabel("Enter OTP:")
        self.otp_input = QLineEdit()
        self.otp_label.hide()  # Hide OTP label initially
        self.otp_input.hide()  # Hide OTP input initially
        self.generated_otp = None   # Hide OTP input initially
        self.otp_sent_time = None 
        # Connect the transfer button click event to send_otp_email function
        self.transfer_button.clicked.connect(self.send_otp_email)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Transfer Money</h2>"))
        layout.addWidget(self.from_account_label)
        layout.addWidget(self.from_account_input)
        layout.addWidget(self.to_account_label)
        layout.addWidget(self.to_account_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.otp_label)
        layout.addWidget(self.otp_input)
        layout.addWidget(self.transfer_button)
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

    def transfer(self):
        # Retrieve account information
        from_account = self.from_account_input.text()
        to_account = self.to_account_input.text()
        amount = self.amount_input.text()

        # Verify OTP
        entered_otp = self.otp_input.text()
        if not entered_otp:
            QMessageBox.critical(
                self,
                "Error",
                "Please enter the OTP received via email.",
            )
            return

        if not self.verify_otp(entered_otp):
            QMessageBox.critical(
                self,
                "Error",
                "Incorrect OTP! Please enter the correct OTP.",
            )
        
            return
        
            if amount > balance:
                    QMessageBox.critical(
                        self,
                        "Error",
                        "Insufficient Balance"
                    )
                    return
        if not from_account or not to_account or not amount:
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
                "Invalid amount! Please enter a valid amount of money.",
            )
            return

        try:
            from_account_balance = self.account_manager.get_balance(from_account)
            if from_account_balance is None:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Account {from_account} not found",
                )
                return
            if amount > from_account_balance:
                QMessageBox.critical(
                    self,
                    "Error",
                    "Insufficient balance in the account",
                )
                return
            
            # Perform the transfer
            self.account_manager.transfer(from_account, to_account, amount)
            QMessageBox.information(
                self,
                "Success",
                f"Successfully transferred {amount} from account {from_account} to account {to_account}."
            )
            self.money_transferred.emit(from_account, to_account, amount)

            # Clear input fields
            self.to_account_input.clear()
            self.from_account_input.clear()

            # Record transactions
            self.account_manager.record_transaction(from_account, "Transfer (Out)", amount)  # Record outgoing transaction
            self.account_manager.record_transaction(to_account, "Transfer (In)", amount)  # Record incoming transaction
        except pyodbc.Error as e:
            error_message = str(e).replace("\n", " ")
            QMessageBox.critical(
                self,
                "Error",
                f"Database Error: {error_message}\nPlease ensure the server and database are correctly configured!",
            )

    def send_otp_email(self):
        # Retrieve account information and validate fields
        from_account = self.from_account_input.text()
        to_account = self.to_account_input.text()
        amount = self.amount_input.text()

        if not from_account or not to_account or not amount:
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
                "Invalid amount! Please enter a valid amount of money.",
            )
            return

        # Get MAC address and email associated with the account number
        mac_address, recipient_email = self.get_mac_address(from_account)
        if not mac_address:
            QMessageBox.critical(
                self,
                "Error",
                f"MAC address not found for account {from_account}",
            )
            return

        # Generate and send OTP via email
        self.generate_and_send_otp(recipient_email, amount)

    def generate_and_send_otp(self, recipient_email, amount):
        try:
            # Generate OTP using TOTP algorithm with a time step of 4 seconds (for testing purposes)
            secret_key_seed = recipient_email.encode('utf-8')  # Using recipient's email as seed for secret key
            secret_key_bytes = secrets.token_bytes(20)  # 20 bytes = 160 bits

            # Derive secret key using PBKDF2-HMAC
            secret_key = hashlib.pbkdf2_hmac('sha1', secret_key_seed, secret_key_bytes, 100000)
            secret_key_base32 = base64.b32encode(secret_key).decode('utf-8')

            totp = pyotp.TOTP(secret_key_base32, interval=10)
            self.generated_otp = totp.now()  # Store the generated OTP
            # Generate the initial OTP
            otp = totp.now()
            self.otp_sent_time = datetime.datetime.now()
            # Sending email with the OTP
            try:
                ob = s.SMTP("smtp.gmail.com", 587)
                ob.starttls()
                ob.login("deepvakharia15@gmail.com", "ykui hqfw klvw dhmb")  # Change to your email and password
                subject = "Your OTP"
                body = f"Your OTP is: {otp}"
                message = f"Subject: {subject}\n\n{body}"
                ob.sendmail(recipient_email, recipient_email, message)  # Change sender and recipient emails
                print("OTP sent successfully.")

                # Show OTP label and input after successfully sending OTP
                self.otp_label.show()
                self.otp_input.show()

                # Inform the user that OTP has been sent
                QMessageBox.information(
                    self,
                    "OTP Sent",
                    "OTP has been sent successfully! Please enter the OTP to proceed with the transfer.",
                    QMessageBox.Ok
                )
            except Exception as e:
                print(f"Error sending OTP: {e}")
            finally:
                ob.quit()
        except Exception as ex:
            print(f"Error occurred: {ex}")

    def verify_otp(self, entered_otp):
        if self.generated_otp is None or self.otp_sent_time is None:
            QMessageBox.critical(
                self,
                "Error",
                "OTP expired. Please regenerate the OTP.",
            )
            return False
        current_time =datetime.datetime.now()
        elapsed_time = (current_time - self.otp_sent_time).seconds

        # Check if the elapsed time is within 5 minutes (10 seconds)
        if elapsed_time > 300:
            QMessageBox.critical(
                self,
                "Error",
                "OTP expired. Please regenerate the OTP.",
            )
            return False

        # Compare entered OTP with the generated OTP
        return entered_otp == self.generated_otp

  

    def get_mac_address(self, account_number):
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

            # Execute the query to get the MAC address and email
            cursor.execute("SELECT a.MAC_Address, a.Email FROM login_log AS l JOIN account AS a ON l.account_number = a.AccountNumber WHERE l.account_number = ?", account_number)

            # Fetch the result
            row = cursor.fetchone()

            # Return the MAC address and email
            if row:
                mac_address = row[0]
                email = row[1]
                return mac_address, email
            else:
                print("No MAC address found for the given account number.")
                return None, None

        except pyodbc.Error as e:
            error_message = str(e).replace("\n", " ")
            print(f"Database Error: {error_message}\nPlease ensure the server and database are correctly configured!")
            return None, None
    
    def go_back_to_main_menu(self):
        self.go_back.emit()
        self.close()