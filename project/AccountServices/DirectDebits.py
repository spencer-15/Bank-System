import sys
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QApplication
)
from decimal import Decimal
from PyQt5.QtWidgets import QDateTimeEdit
from PyQt5.QtCore import Qt, QDateTime, QTimer
from connection import AccountManager  
from PyQt5.QtCore import pyqtSignal
import pyodbc

class RecurringPaymentsWidget(QWidget):
    go_back = pyqtSignal()

    def __init__(self, account_manager):
        super().__init__()

        self.setWindowTitle("Recurring Payments and Direct Debits")
        self.setGeometry(100, 100, 800, 600)

        self.account_manager = account_manager  # Pass AccountManager instance

        self.type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Recurring Payment", "Direct Debit"])
        self.type_combo.currentIndexChanged.connect(self.update_ui)

        self.details_label = QLabel("Details:")
        self.details_input = QLineEdit()

        self.amount_label = QLabel("Amount:")
        self.amount_input = QLineEdit()

        self.interval_label = QLabel("Interval (days):")
        self.interval_input = QLineEdit()

        self.datetime_label = QLabel("Setup Date and Time:")
        self.datetime_picker = QDateTimeEdit()
        self.datetime_picker.setDateTime(QDateTime.currentDateTime())
        self.datetime_picker.setDisplayFormat("yyyy-MM-dd HH:mm:ss")

        self.setup_recurring_button = QPushButton("Setup Recurring Payment")
        self.setup_recurring_button.clicked.connect(self.setup_payment)

        self.setup_direct_debit_button = QPushButton("Setup Direct Debit")
        self.setup_direct_debit_button.clicked.connect(self.setup_direct_debit)

        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(4)
        self.payment_table.setHorizontalHeaderLabels(["Type", "Details", "Amount", "Setup Date and Time"])

        self.direct_debit_widget = QWidget()
        self.direct_debit_layout = QVBoxLayout()
        self.membership_id_label = QLabel("Membership ID:")
        self.membership_id_input = QLineEdit()
        self.fee_label = QLabel("Membership Fee:")
        self.fee_input = QLineEdit()
        self.setup_direct_debit_layout = QVBoxLayout()
        self.setup_direct_debit_layout.addWidget(QLabel("<h2>Direct Debits - Membership Fees</h2>"))
        self.setup_direct_debit_layout.addWidget(self.membership_id_label)
        self.setup_direct_debit_layout.addWidget(self.membership_id_input)
        self.setup_direct_debit_layout.addWidget(self.fee_label)
        self.setup_direct_debit_layout.addWidget(self.fee_input)
        self.setup_direct_debit_layout.addWidget(self.setup_direct_debit_button)
        self.direct_debit_widget.setLayout(self.setup_direct_debit_layout)
        self.direct_debit_widget.setVisible(False)

        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; width: 80px;")
        self.back_button.clicked.connect(self.go_back_to_main_menu)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Recurring Payments and Direct Debits</h2>"))
        layout.addWidget(self.type_label)
        layout.addWidget(self.type_combo)
        layout.addWidget(self.details_label)
        layout.addWidget(self.details_input)
        layout.addWidget(self.amount_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(self.datetime_label)
        layout.addWidget(self.datetime_picker)
        layout.addWidget(self.setup_recurring_button)
        layout.addWidget(self.payment_table)
        layout.addWidget(self.direct_debit_widget)

        # Add a horizontal layout for the back button
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.back_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.fetch_account_number_button = QPushButton("Fetch Account Number")
        self.fetch_account_number_button.clicked.connect(self.fetch_account_number)

        # Timer to check and process overdue payments every minute
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.process_overdue_payments)
        self.timer.start(60000)  # 60000 milliseconds = 1 minute

    def fetch_account_number(self):
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

            # Execute a query to retrieve the account number from the login_log table
            cursor.execute("SELECT TOP 1 account_number FROM login_log ORDER BY login_time DESC")
            
            row = cursor.fetchone()

            # Check if a row was returned
            if row:
                account_number = row[0]
                print("Account Number DirectDebits :", account_number)
                
            else:
                QMessageBox.warning(self, "Warning", "No account number found in login log.")
            
            # Close the cursor and connection
            cursor.close()
            connection.close()
            return account_number  # Return the fetched account number
        except pyodbc.Error as e:
            QMessageBox.warning(self, "Error", f"Error fetching account number: {e}")

    def go_back_to_main_menu(self):
        self.go_back.emit()
        self.close()

    def update_ui(self):
        if self.type_combo.currentText() == "Direct Debit":
            self.hide_recurring_payment_widgets()
            self.direct_debit_widget.setVisible(True)
        else:
            self.show_recurring_payment_widgets()
            self.direct_debit_widget.setVisible(False)

    def hide_recurring_payment_widgets(self):
        self.details_label.hide()
        self.details_input.hide()
        self.amount_label.hide()
        self.amount_input.hide()
        self.interval_label.hide()
        self.interval_input.hide()
        self.datetime_label.hide()
        self.datetime_picker.hide()
        self.setup_recurring_button.hide()

    def show_recurring_payment_widgets(self):
        self.details_label.show()
        self.details_input.show()
        self.amount_label.show()
        self.amount_input.show()
        self.interval_label.show()
        self.interval_input.show()
        self.datetime_label.show()
        self.datetime_picker.show()
        self.setup_recurring_button.show()

    def setup_payment(self):
        payment_type = self.type_combo.currentText()
        details = self.details_input.text()
        amount = Decimal(self.amount_input.text())
        
        setup_datetime = self.datetime_picker.dateTime().toString(Qt.ISODate)

        if not details or not amount:
            QMessageBox.warning(self, "Error", "Please fill in all the fields.")
            return

        try:
            account_number = self.fetch_account_number()
            cursor = self.account_manager.connection.cursor()
            cursor.execute("SELECT a.Balance FROM account a INNER JOIN login_log l ON a.AccountNumber = l.account_number WHERE l.account_number = ?;", (account_number,))
            row = cursor.fetchone()
            if row:
                current_balance = row[0]
                new_balance = current_balance - amount  # Subtract the amount from the current balance
                
                # Update the balance in the database
                cursor.execute("UPDATE account SET Balance = ? WHERE AccountNumber = ?", (new_balance, account_number))
                self.account_manager.connection.commit()  # Commit the transaction

                # Insert payment record into the table
                cursor.execute("INSERT INTO payment (Type, Details, Amount, SetupDateTime) VALUES (?, ?, ?, ?);", (payment_type, details, amount, setup_datetime))
                self.account_manager.connection.commit()  # Commit the transaction

                row_position = self.payment_table.rowCount()
                self.payment_table.insertRow(row_position)
                self.payment_table.setItem(row_position, 0, QTableWidgetItem(payment_type))
                self.payment_table.setItem(row_position, 1, QTableWidgetItem(details))
                self.payment_table.setItem(row_position, 2, QTableWidgetItem(str(amount)))  # Convert amount to string for table
                self.payment_table.setItem(row_position, 3, QTableWidgetItem(setup_datetime))  # Index should be 3
                QMessageBox.information(self, "Payment Setup", "Your recurring payment/direct debit has been set up successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to setup payment: {str(e)}")

        # Clear input fields after submitting request
        self.details_input.clear()
        self.amount_input.clear()

        # Fetch and print account number
        self.fetch_account_number()

    def setup_direct_debit(self):
        membership_id = self.membership_id_input.text()
        fee = Decimal(self.fee_input.text())
        setup_datetime = self.datetime_picker.dateTime().toString(Qt.ISODate)

        if not membership_id or not fee:
            QMessageBox.warning(self, "Error", "Please fill in all the fields.")
            return

        try:
            account_number = self.fetch_account_number()
            # Fetch the current balance
            cursor = self.account_manager.connection.cursor()
            cursor.execute("SELECT a.Balance FROM account a INNER JOIN login_log l ON a.AccountNumber = l.account_number WHERE l.account_number = ?;", (account_number,))
            row = cursor.fetchone()
            if row:
                current_balance = row[0]
                new_balance = current_balance - fee  # Subtract the fee from the current balance

                # Update the balance in the database
                cursor.execute("UPDATE account SET Balance = ? WHERE AccountNumber = ?", (new_balance, account_number))
                self.account_manager.connection.commit()  # Commit the transaction

                # Insert direct debit record into the table
                cursor.execute("INSERT INTO direct_debit (MembershipID, Fee, SetupDateTime) VALUES (?, ?, ?);", (membership_id, fee, setup_datetime))
                self.account_manager.connection.commit()  # Commit the transaction

                row_position = self.payment_table.rowCount()
                setup_datetime = self.datetime_picker.dateTime().toString(Qt.ISODate)
                self.payment_table.insertRow(row_position)
                self.payment_table.setItem(row_position, 0, QTableWidgetItem("Direct Debit"))
                self.payment_table.setItem(row_position, 1, QTableWidgetItem(membership_id))
                self.payment_table.setItem(row_position, 2, QTableWidgetItem(str(fee)))  # Convert fee to string for table
                self.payment_table.setItem(row_position, 3, QTableWidgetItem(setup_datetime))
                QMessageBox.information(self, "Direct Debit Setup", "Direct debit for membership fee has been set up successfully.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to setup direct debit: {str(e)}")

        # Clear input fields after submitting request
        self.membership_id_input.clear()
        self.fee_input.clear()

        # Fetch and print account number
        self.fetch_account_number()

    def process_overdue_payments(self):
        try:
            cursor = self.account_manager.connection.cursor()
            current_datetime = QDateTime.currentDateTime()
            # Fetch payments where the setup date and time is before the current date and time
            cursor.execute("SELECT * FROM payment WHERE SetupDateTime <= ? AND Processed = 0;", (current_datetime.toString(Qt.ISODate),))
            overdue_payments = cursor.fetchall()
            
            for payment in overdue_payments:
                payment_id, payment_type, details, amount, setup_datetime = payment
                account_number = self.fetch_account_number()  # Fetch the account number
                cursor.execute("SELECT Balance FROM account WHERE AccountNumber = ?;", (account_number,))
                row = cursor.fetchone()
                if row:
                    current_balance = row[0]
                    new_balance = current_balance - amount
                    cursor.execute("UPDATE account SET Balance = ? WHERE AccountNumber = ?;", (new_balance, account_number))
                    
                    # Mark the payment as processed
                    cursor.execute("UPDATE payment SET Processed = 1 WHERE PaymentID = ?;", (payment_id,))
                    
                    self.account_manager.connection.commit()  # Commit the transaction
        except Exception as e:
            print(f"Error processing overdue payments: {str(e)}")


    def closeEvent(self, event):
            # Close database connection when closing the application
        self.account_manager.close_connection()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    account_manager = AccountManager(server=r"NAMASTE\SQLEXPRESS", database="BankSystem")  
    window = RecurringPaymentsWidget(account_manager)
    window.show()
    sys.exit(app.exec_())
