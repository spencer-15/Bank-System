
#Homepage.py
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
import sys
import pyodbc

from gui import MainMenuWidget, LoginWidget
from connection import AccountManager
from Login_form import AdvancedLoginForm


def clear_login_log():
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

        # Execute SQL query to clear the login_log table
        cursor.execute("DELETE FROM login_log")

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()
    except pyodbc.Error as e:
        print("Error clearing login log:", e)


class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Home Page")
        self.setGeometry(100, 100, 400, 300)
        self.setObjectName('Home Page') 
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("background-color: #4CAF50; color: white")
        self.login_button.clicked.connect(self.show_login_form)
        self.hide()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h1>Welcome to Banking System</h1>"))
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        self.login_form = AdvancedLoginForm()
        self.login_form.setWindowTitle("Login")

    def show_login_form(self):
        self.login_form.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(clear_login_log)
    home_page = HomePage()
    home_page.show()
    sys.exit(app.exec_())
