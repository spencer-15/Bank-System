#main_menue.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap, QTransform, QIcon
from PyQt5.QtCore import pyqtSignal, Qt
from AccountManagement.AccountHandling import AccountWindow
from FinancialTransactions.FinancialHandling import FinancialWidget
from AccountServices.ServicesHandling import ServicesWidget
from Helpdesk.handle import HelpHandleMain
class MyWindow(QWidget):
    go_back = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Menue")
        self.setGeometry(100, 100, 400, 300)

        self.button_layout = QGridLayout()

        self.Account_button = QPushButton("Account Management", self)
        self.Account_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #3e8e41; }"
                                      "QPushButton:pressed { background-color: #2e7d32; }")
        
        self.button_layout.addWidget(self.Account_button, 0, 0, 1, 2)

        self.financial_button = QPushButton("Financial Transactions ", self)
        self.financial_button.setStyleSheet("QPushButton { background-color: #00bcd4; color: white; font-size: 14px; }"
                                        "QPushButton:hover { background-color: #0097a7; }"
                                        "QPushButton:pressed { background-color: #00838f; }")
        self.button_layout.addWidget(self.financial_button, 1, 0, 1, 2)

        self.account_service_button = QPushButton("Account Services ", self)
        self.account_service_button.setStyleSheet("QPushButton { background-color: #009688; color: white; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #00796b; }"
                                      "QPushButton:pressed { background-color: #00695c; }")
        self.button_layout.addWidget(self.account_service_button, 2, 0, 1, 2)

        self.back_button = QPushButton("Back", self)
        self.back_button.setStyleSheet("QPushButton { background-color: #f44336; color: white; font-size: 14px; width: 80px; }"
                                      "QPushButton:hover { background-color: #e53935; }"
                                      "QPushButton:pressed { background-color: #d32f2f; }")
        self.button_layout.addWidget(self.back_button, 4, 0, 1, 2)
        self.Help_button = QPushButton("Help desk", self)
        self.Help_button.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-size: 14px; }"
                                      "QPushButton:hover { background-color: #3e8e41; }"
                                      "QPushButton:pressed { background-color: #2e7d32; }")
        self.button_layout.addWidget(self.Help_button, 3, 0, 1, 2)
        
        
        
        spacer = QLabel("", self)
        self.button_layout.addWidget(spacer, 3, 1, 1, 1)
        
        self.setLayout(self.button_layout)
    
        font = QFont("Arial", 14)
        self.Account_button.setFont(font)
        self.financial_button.setFont(font)
        self.account_service_button.setFont(font)
        self.Help_button.setFont(font)
        self.back_button.setFont(font)

        pixmap = QPixmap("back_icon.png")
        transform = QTransform()
        back_icon = QIcon(pixmap.transformed(transform))
        self.back_button.setIcon(back_icon)
        self.back_button.clicked.connect(self.go_back_to_main_menu)
        
        self.account_form = AccountWindow()
        self.Account_button.clicked.connect(self.account_form.show)
        
        self.financial_form = FinancialWidget()
        self.financial_button.clicked.connect(self.financial_form.show)
        
        self.account_services_form = ServicesWidget()
        self.account_service_button.clicked.connect(self.account_services_form.show)
        
        self.helphandle_form = HelpHandleMain()
        self.Help_button.clicked.connect(self.helphandle_form.show)
        
    def financial_form(self):
        self.financial_form.show()
        self.close()    
    def account_form(self):
        self.account_form.show()
        self.close()
    
    def account_services_form(self):
        self.account_services_form.show()
        self.close()   
    
    def helphandle_form(self):
        self.helphandle_form.show()
        self.close
        
    def go_back_to_main_menu(self):
        self.go_back.emit()
        
        self.close()
    
    
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyWindow()
    window.show()

    sys.exit(app.exec_())
