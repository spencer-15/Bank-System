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
    QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal
import pyodbc
from PyQt5.QtGui import QFont, QPixmap, QTransform, QIcon
from AccountManagement.AccountHandling import AccountWindow
from connection import AccountManager
from AccountServices.DirectDebits import RecurringPaymentsWidget
from AccountServices.ViewDetailed import AccountServicesHistory
from AccountServices.services import ServiceRequestWidget

class ServicesWidget(QWidget):
    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Services")
        self.setGeometry(100, 100, 400, 300)

        self.button_layout = QGridLayout()

        self.services_button = QPushButton("Services", self)
        self.services_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #3e8e41; }"
                                      "QPushButton:pressed { background-color: #2e7d32; }")

        self.button_layout.addWidget(self.services_button, 0, 0, 1, 2)

        self.repeatpay_button = QPushButton("RepeatPay", self)
        self.repeatpay_button.setStyleSheet("QPushButton { background-color: #00bcd4; color: white; font-size: 14px; }"
                                        "QPushButton:hover { background-color: #0097a7; }"
                                        "QPushButton:pressed { background-color: #00838f; }")

        self.button_layout.addWidget(self.repeatpay_button, 1, 0, 1, 2)

        self.viewdetailed_button = QPushButton("View Detailed Account", self)
        self.viewdetailed_button.setStyleSheet("QPushButton { background-color: #009688; color: white; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #00796b; }"
                                      "QPushButton:pressed { background-color: #00695c; }")

        self.button_layout.addWidget(self.viewdetailed_button, 3, 0, 1, 2)

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
        self.history_table.setColumnCount(6)  # Increase column count to 6 for Account Type
        self.history_table.setHorizontalHeaderLabels(["Transaction ID", "Account Number", "Transaction Type", "Amount", "Date", "Account Type"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.account_manager = AccountManager(server=r"NAMASTE\SQLEXPRESS", database="BankSystem")

        self.services_widget = ServiceRequestWidget() 
        self.services_widget.go_back.connect(self.show)
        
        self.repeatpay_widget = RecurringPaymentsWidget(self.account_manager)  
        self.repeatpay_widget.go_back.connect(self.show)

        self.history_widget = AccountServicesHistory(self.account_manager)
        self.history_widget.go_back.connect(self.show)

        font = QFont("Arial", 14)
        self.services_button.setFont(font)
        self.repeatpay_button.setFont(font)
        self.viewdetailed_button.setFont(font)
        self.back_button.setFont(font)

        self.back_button.clicked.connect(self.go_back_to_main_menu)
        self.services_button.clicked.connect(self.show_Services_form)
        self.repeatpay_button.clicked.connect(self.show_repeatpay_form)
        self.viewdetailed_button.clicked.connect(self.show_history_form)
        self.viewdetailed_button.clicked.connect(lambda:self.load_history(None))
    def show_Services_form(self):
        self.services_widget.show()
        self.close()

    def show_repeatpay_form(self):
        self.repeatpay_widget.show()
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

    def go_back_to_main_menu(self):
        self.go_back.emit()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ServicesWidget()
    window.show()
    sys.exit(app.exec_())
