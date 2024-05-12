from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QApplication,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import pyodbc
import sys


class GetAccountInfoWidget(QWidget):
    account_info_fetched = pyqtSignal(dict)
    go_back = pyqtSignal()

    def __init__(self, account_manager,account_number=None):
        super().__init__()
        
        self.account_number = account_number
        self.setWindowTitle("Get Account Information")
        self.setGeometry(100, 100, 600, 400)

        self.account_manager = account_manager

        self.account_number_label = QLabel("Account Number:")
        self.account_number_input = QLineEdit()
        self.account_number_input.setText(self.account_number)
        self.get_info_button = QPushButton("Get Account Information")
        self.back_button = QPushButton("Back to Home")
        self.get_info_button.clicked.connect(self.get_account_info)
        self.back_button.clicked.connect(self.go_back_to_main_menu)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)
        self.table_widget.setHorizontalHeaderLabels(["Attribute", "Value"])
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Get Account Information</h2>"))
        layout.addWidget(self.account_number_label)
        layout.addWidget(self.account_number_input)
        layout.addWidget(self.get_info_button)
        layout.addWidget(self.table_widget)
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

    def get_account_info(self):
        account_number = self.account_number_input.text()

        if not account_number:
            QMessageBox.critical(
                self,
                "Error",
                "Please fill in the Account Number field!",
            )
            return

        try:
            account_info_row = self.account_manager.get_account(account_number)
            if account_info_row:
                account_info = {}
                for index, column in enumerate(account_info_row.cursor_description):
                    column_name = column[0]
                    column_value = account_info_row[index]  # Access by index
                    account_info[column_name] = column_value
                
                # Clear existing table contents
                self.table_widget.setRowCount(0)
                
                # Populate the table with the account information
                for key, value in account_info.items():
                    row_position = self.table_widget.rowCount()
                    self.table_widget.insertRow(row_position)
                    self.table_widget.setItem(row_position, 0, QTableWidgetItem(key))
                    self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(value)))
                    
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    account_manager = None  # Initialize your account manager here
    widget = GetAccountInfoWidget(account_manager)
    widget.show()
    sys.exit(app.exec_())
