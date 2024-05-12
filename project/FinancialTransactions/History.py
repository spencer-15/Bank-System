from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QHeaderView,
    QHBoxLayout,
    QPushButton,
)
from PyQt5.QtCore import Qt, pyqtSignal
import pyodbc

class TransactionHistoryWidget(QWidget):
    go_back = pyqtSignal()

    def __init__(self, account_manager):
        super().__init__()

        self.setWindowTitle("Transaction History")
        self.setGeometry(100, 100, 800, 600)

        self.account_manager = account_manager

        self.history_label = QLabel("<h2>Transaction History</h2>")
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)  # Added one more column for date
        self.history_table.setHorizontalHeaderLabels(["Transaction ID", "Account Number", "Transaction Type", "Amount", "Date"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.back_button = QPushButton("Back to Home")

        layout = QVBoxLayout()
        layout.addWidget(self.history_label)
        layout.addWidget(self.history_table)
        
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.back_button)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

        self.back_button.clicked.connect(self.go_back_to_main_menu)

    def set_account_number(self, account_number):
        self.load_history(account_number)

    def load_history(self, account_number):
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
