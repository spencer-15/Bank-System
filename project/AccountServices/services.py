from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,  # Import QHBoxLayout for horizontal layout
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QApplication,
    QSpacerItem,  # Import QSpacerItem for spacing
    QSizePolicy   # Import QSizePolicy for controlling the size policy of widgets
)
from PyQt5.QtCore import pyqtSignal

class ServiceRequestWidget(QWidget):
    go_back = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Service Requests")
        self.setGeometry(100, 100, 600, 400)

        self.request_label = QLabel("Select Service:")
        self.request_combo = QComboBox()
        self.request_combo.addItems(["Checkbook", "Debit Card", "Credit Card"])

        self.details_label = QLabel("Additional Details:")
        self.details_input = QLineEdit()

        self.request_button = QPushButton("Submit Request")

        self.request_button.clicked.connect(self.submit_request)

        self.request_table = QTableWidget()
        self.request_table.setColumnCount(3)
        self.request_table.setHorizontalHeaderLabels(["Service", "Details", "Status"])
        
        # Back button
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("background-color: #f44336; color: white; font-size: 14px; width: 80px;")
        self.back_button.clicked.connect(self.go_back_to_main_menu)
        
        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button)
        button_layout.addStretch(1)  # Add a stretchable space to push the back button to the left
        
        # Create vertical layout for other widgets
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Service Requests</h2>"))
        layout.addWidget(self.request_label)
        layout.addWidget(self.request_combo)
        layout.addWidget(self.details_label)
        layout.addWidget(self.details_input)
        layout.addWidget(self.request_button)
        layout.addWidget(self.request_table)
        
        # Add button layout to the main layout
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

    def submit_request(self):
        service = self.request_combo.currentText()
        details = self.details_input.text()

        row_position = self.request_table.rowCount()
        self.request_table.insertRow(row_position)
        self.request_table.setItem(row_position, 0, QTableWidgetItem(service))
        self.request_table.setItem(row_position, 1, QTableWidgetItem(details))
        self.request_table.setItem(row_position, 2, QTableWidgetItem("Pending"))
        
        QMessageBox.information(self, "Request Submitted", "Your request will be processed within 10 days.")
        
        # Clear input fields after submitting request
        self.details_input.clear()
        
    def go_back_to_main_menu(self):
        self.go_back.emit()
        self.close()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ServiceRequestWidget()
    window.show()
    sys.exit(app.exec_())
