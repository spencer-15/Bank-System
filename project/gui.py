# gui.py
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
)
import sys
from AccountManagement.CreateAccount import CreateAccountWidget
from connection import AccountManager
from AccountManagement.UpdateAccount import UpdateAccountWidget

class MainMenuWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Banking System")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")
        self. cre_account_widget = None
        self.create_account_button = QPushButton("Create Account")
        self.update_account_button = QPushButton("Update Account")
        self.delete_account_button = QPushButton("Delete Account")
        self.deposit_button = QPushButton("Deposit")
        self.withdraw_button = QPushButton("Withdraw")
        self.transfer_button = QPushButton("Transfer")
        self.exit_button = QPushButton("Exit")

        self.create_account_button.clicked.connect(self.create_account)
        self.update_account_button.clicked.connect(self.update_account)
        self.delete_account_button.clicked.connect(self.handle_delete_account)
        self.deposit_button.clicked.connect(self.handle_deposit)
        self.withdraw_button.clicked.connect(self.handle_withdraw)
        self.transfer_button.clicked.connect(self.handle_transfer)
        self.exit_button.clicked.connect(self.close)

        self.style_buttons()

        layout = QVBoxLayout()
        layout.addWidget(QLabel("<h2 style='color: #0040ff;'>Banking System</h2>"))
        layout.addWidget(self.create_account_button)
        layout.addWidget(self.update_account_button)
        layout.addWidget(self.delete_account_button)
        layout.addWidget(self.deposit_button)
        layout.addWidget(self.withdraw_button)
        layout.addWidget(self.transfer_button)
        layout.addWidget(self.exit_button)
        layout.addStretch()

        self.setLayout(layout)

    def style_buttons(self):
        button_list = [
            self.create_account_button,
            self.update_account_button,
            self.delete_account_button,
            self.deposit_button,
            self.withdraw_button,
            self.transfer_button,
            self.exit_button,
        ]

        for button in button_list:
            button.setStyleSheet(
                "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px; padding: 10px;}"
                "QPushButton:hover { background-color: #45a049; }"
                "QPushButton:pressed { background-color: #367d3a; }"
            )

    def create_account(self):
        self.hide()
        server = r"NAMASTE\SQLEXPRESS"
        database = "BankSystem"
        account_manager = AccountManager(server, database)
        self.create_account_widget = CreateAccountWidget(account_manager)
        self.create_account_widget.account_created.connect(self.handle_account_created)
        self.create_account_widget.go_back.connect(self.show_main_menu)

        self.create_account_widget.show()

    def show_main_menu(self):
        self.create_account_widget.close()
        self.show()

    def handle_account_created(self, account_number, account_type):
        QMessageBox.information(self, "Success", "Account created successfully.")

    def update_account(self):
        self.hide()
        server = r"NAMASTE\SQLEXPRESS"
        database = "BankSystem"
        account_manager = AccountManager(server, database)
        self.UpdateAccountWidget = UpdateAccountWidget(account_manager)
        self.UpdateAccountWidget.account_updated.connect(self.handle_account_update)
        self.UpdateAccountWidget.go_back.connect(self.show_main_menu)
        self.UpdateAccountWidget.show()

    def show_main_menu(self):
        self.UpdateAccountWidget.close()
        self.show()

    def handle_account_update(self, account_number, account_type):
        QMessageBox.information(self, "Success", "Account updated successfully.")

    def handle_delete_account(self):
        print("Delete Account button clicked")

    def handle_deposit(self):
        print("Deposit button clicked")

    def handle_withdraw(self):
        print("Withdraw button clicked")

    def handle_transfer(self):
        print("Transfer button clicked")


class LoginWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.show_main_menu)

        self.style_login_button()

        layout = QVBoxLayout()
        layout.addWidget(
            QLabel("<h2 style='color: #0040ff;'>Welcome to Banking System</h2>")
        )
        layout.addWidget(self.login_button)
        layout.addStretch()

        self.setLayout(layout)

    def style_login_button(self):
        self.login_button.setStyleSheet(
            "QPushButton { background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px; padding: 10px;}"
            "QPushButton:hover { background-color: #45a049; }"
            "QPushButton:pressed { background-color: #367d3a; }"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_widget = LoginWidget()
    login_widget.show()
    sys.exit(app.exec_())

