
#login.py
from PyQt5.QtWidgets import(    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QMessageBox,
    
)
import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import pyodbc
from connection import AccountManager
from main_menue import MyWindow
from AccountManagement.CreateAccount import CreateAccountWidget

class LoginFormStyle:
    go_back = pyqtSignal()
    def __init__(self):
        self.STYLESHEET = """
            QLabel {
                color: #333;
                font-weight: bold;
                font-size: 14px;
            }

            QLineEdit {
                border: 1px solid #ccc;
                padding: 4px;
                font-size: 14px;
            }

            QPushButton {
                background-color: #5c3d88;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #4a2f6d;
            }

            QMessageBox {
                background-color: #f0f0f0;
            }

            QMessageBox QLabel {
                color: #333;
                font-weight: bold;
                font-size: 16px;
            }

            .button-effect {
                padding: 10px;
                border-radius: 10px;
                background-color: rgba(0, 0, 0, 0);
            }
        """

    def apply_style(self, widget):
        widget.setStyleSheet(self.STYLESHEET)


class AdvancedLoginForm(QWidget):
    account_number_emitted = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.style = LoginFormStyle()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setWindowIcon(QIcon("icon.png"))
        self.setGeometry(300, 300, 400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.layout = QGridLayout()

        # Add logo
        logo_label = QLabel()
        logo_label.setPixmap(QIcon("logo.png").pixmap(80, 80))
        self.layout.addWidget(logo_label, 0, 0, 1, 2)

        # Add account type label and input
        Name_label = QLabel(" Name ")
        Name_label.setStyleSheet("color: #333; font-weight: bold;")
        self.Name_input = QLineEdit()
        self.Name_input.setPlaceholderText("Enter your Name")
        self.Name_input.setStyleSheet("border: 1px solid #ccc; padding: 4px;")
        self.layout.addWidget(Name_label, 1, 0)
        self.layout.addWidget(self.Name_input, 1, 1)

        # Add account number label and input
        Email_label = QLabel(" Email ")
        Email_label.setStyleSheet("color: #333; font-weight: bold;")
        self.Email_input = QLineEdit()
        self.Email_input.setPlaceholderText("Enter your Email")
        self.Email_input.setStyleSheet("border: 1px solid #ccc; padding: 4px;")
        self.layout.addWidget(Email_label, 2, 0)
        self.layout.addWidget(self.Email_input, 2, 1)
        
        # Add account number label and input
        Password_label = QLabel(" Password ")
        Password_label.setStyleSheet("color: #333; font-weight: bold;")
        self.Password_input = QLineEdit()
        self.Password_input.setPlaceholderText("Enter your Password")
        self.Password_input.setStyleSheet("border: 1px solid #ccc; padding: 4px;")
        self.Password_input.setEchoMode(QLineEdit.Password)
        self.show_password_button = QPushButton("Show Password")
        self.show_password_button.clicked.connect(self.password_visibility)
        self.layout.addWidget(Password_label, 3, 0)
        self.layout.addWidget(self.Password_input, 3, 1)
        # Add buttons
        self.login_button = QPushButton("Login")
        self.create_button = QPushButton("Create Account")
        self.login_button.setStyleSheet("background-color: #5c3d88; color: white; padding: 8px; border: none; border-radius: 4px; font-weight: bold;")
        self.create_button.setStyleSheet("background-color:Green;color:white;padding:8px;border:none;border-radius:4px;font-weight:bold;")
        self.layout.addWidget(self.show_password_button,3,2)
        self.layout.addWidget(self.login_button, 4, 0, 1, 2)
        self.layout.addWidget(self.create_button, 5, 0, 1, 2)
       
        self.setLayout(self.layout)
        
     
        self.style.apply_style(self)

        self.login_button.clicked.connect(self.handle_login_click)
        self.login_button.clicked.connect(self.clear_fileds)
        
        self.create_button.clicked.connect(self.create_account)

    def create_account(self):
        self.hide()
        server = r"NAMASTE\SQLEXPRESS"
        database = "BankSystem"
        account_manager = AccountManager(server, database)
        self.create_account_widget = CreateAccountWidget(account_manager)
        self.create_account_widget.account_created.connect(self.handle_account_created)
        self.create_account_widget.go_back.connect(self.show_main_menu)

        self.create_account_widget.show()
    def clear_fileds(self):
        self.Name_input.clear()
        self.Email_input.clear()
        self.Password_input.clear()
    def show_main_menu(self):
        self.create_account_widget.close()
        self.show()

    def handle_account_created(self, Name,Email,Password):
        QMessageBox.information(self, "Success", "Account created successfully.")
        self.hide()
        
    def handle_login_click(self):
        Name = self.Name_input.text()
        Email = self.Email_input.text()
        Password = self.Password_input.text()

        print(f"Name: {Name}, Email: {Email}, Password: {Password}")  # Debugging

        if not Name:
            QMessageBox.warning(
                self,
                "Warning",
                "Please enter your Name",
            )
            return
        elif not Email:
            QMessageBox.warning(
                self,
                "warning",
                "please enter correct email"      
            )
            return
        elif not Password:
            QMessageBox.warning(
                self,
                "warning",
                "please enter correct password"
            )
            return

        # Connect to the database and execute a query to check account existence
        try:
            connection = pyodbc.connect(
                driver="{SQL Server}",
                server=r"NAMASTE\SQLEXPRESS",  # User name
                database="BankSystem",  # database name
                trusted_connection="yes",
            )

            cursor = connection.cursor()

            # Execute a query to check if the account exists
            cursor.execute(
                "SELECT * FROM account WHERE Name = ? AND Email = ? AND Password = ?",
                (Name, Email, Password),
            )
            
            rows = cursor.fetchall()  # Debugging
            print("Rows:", rows)  # Debugging

            if rows:
                QMessageBox.information(
                    self,
                    "Success",
                    f"Welcome! You are now logged in with Name {Name}, Email {Email}, and Password {Password}.",
                )

                # Print the relevant account number (assuming it's in the second column of the row)
                account_number = rows[0][7]
                user_name = rows[0][1]
                print("Account Number:", account_number)
                cursor.execute("INSERT INTO login_log (account_number,Name) VALUES (?,?)",
                (account_number,user_name,))
                connection.commit()
                self.hide()
                self.MyWindow = MyWindow()
                self.MyWindow.show()
            else:
                # Check separately for each field if it exists in the database
                cursor.execute("SELECT * FROM account WHERE Name = ?", (Name,))
                name_row = cursor.fetchall()
                if not name_row:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Invalid Name. Please try again."
                    )
                    return
                cursor.execute("SELECT * FROM account WHERE Email = ?", (Email,))
                email_row = cursor.fetchall()
                print("email row from database :", email_row)
                if not email_row:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Invalid Email. Please try again."
                    )
                    return

                cursor.execute("SELECT * FROM account WHERE Password = ?", (Password,))
                password_row = cursor.fetchall()
                if not password_row:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        "Invalid Password. Please try again."
                    )
                    return
                    
        except Exception as e:
            print("Error:", e)

        self.previous_form = None
    
    def password_visibility(self):
        if self.Password_input.echoMode() == QLineEdit.Password:
            self.Password_input.setEchoMode(QLineEdit.Normal)  # Show password
            self.show_password_button.setText("Hide Password")
        else:
            self.Password_input.setEchoMode(QLineEdit.Password)  # Hide password
            self.show_password_button.setText("Show Password")    
    def show_previous_form(self):
        if self.previous_form:
            self.previous_form.show()
        self.close()    
if __name__ == "__main__":
    app = QApplication(sys.argv)

    demo = AdvancedLoginForm()
    demo.show()

    sys.exit(app.exec_())
