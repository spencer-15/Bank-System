from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QTextEdit, QLabel, QMessageBox
import pyodbc
from datetime import datetime
from PyQt5.QtCore import pyqtSignal, Qt
class ReportIssueWidget(QWidget):
    go_back = pyqtSignal()
    def __init__(self, user_name=None, account_number=None):
        super().__init__()
        self.setWindowTitle("Report Issue")
        self.setGeometry(100, 100, 600, 400)
        
        self.user_name = user_name
        self.account_number = account_number

        self.user_name_label = QLabel("User Name:")
        self.user_name_textedit = QTextEdit()
        self.user_name_textedit.setReadOnly(True)
        self.user_name_textedit.setPlainText(self.user_name)

        self.account_number_label = QLabel("Account Number:")
        self.account_number_textedit = QTextEdit()
        self.account_number_textedit.setReadOnly(True)
        self.account_number_textedit.setPlainText(self.account_number)

        self.issue_label = QLabel("Describe the issue or fraudulent activity:")
        self.issue_textedit = QTextEdit()

        self.report_button = QPushButton("Report Issue")
        self.report_button.clicked.connect(self.report_issue)
        
        self.back_button = QPushButton("BACK")
        self.back_button.clicked.connect(self.go_back_button)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2>Report Issue</h2>"))
        layout.addWidget(self.user_name_label)
        layout.addWidget(self.user_name_textedit)
        layout.addWidget(self.account_number_label)
        layout.addWidget(self.account_number_textedit)
        layout.addWidget(self.issue_label)
        layout.addWidget(self.issue_textedit)
        layout.addWidget(self.report_button)
        layout.addWidget(self.back_button)
        self.setLayout(layout)
    def report_issue(self):
        issue_description = self.issue_textedit.toPlainText().strip()
        if issue_description:
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

                # Execute a query to insert the reported issue into the database
                cursor.execute("INSERT INTO ReportedIssues (UserName, AccountNumber, IssueDescription, ReportedDate) VALUES (?, ?, ?, ?)",
                            (self.user_name, self.account_number, issue_description, datetime.now()))

                # Commit the transaction
                connection.commit()

                # Close the cursor and connection
                cursor.close()
                connection.close()

                QMessageBox.information(self, "Issue Reported", "Your issue has been reported successfully.")
                self.go_back.emit()  # Emit the go_back signal instead of closing the widget
            except pyodbc.Error as e:
                QMessageBox.warning(self, "Database Error", f"Error reporting issue: {e}")
        else:
            QMessageBox.warning(self, "Incomplete Information", "Please describe the issue before reporting.")

    def go_back_button(self):
            self.go_back.emit()
            self.close()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    report_issue_widget = ReportIssueWidget()
    report_issue_widget.show()

    sys.exit(app.exec_())
