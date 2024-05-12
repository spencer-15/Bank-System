from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox, QSizePolicy
from PyQt5.QtCore import pyqtSignal, Qt

class HelpdeskWidget(QWidget):
    go_back = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Integrated Helpdesk")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        self.title_label = QLabel("<h2>Integrated Helpdesk</h2>")
        self.layout.addWidget(self.title_label)

        self.question_buttons = []
        self.answer_texts = []
        questions = [
            "Question 1: How do I create a new account?",
            "Question 2: Can I edit my account information?",
            "Question 3: How can I deposit funds into my account?",
            "Question 4: What should I do if I want to transfer money to another account?",
            "Question 5: How can I view my account balance?",
            "Question 6: What do I do if I forget my login credentials?",
            "Question 7: Is my personal information secure on this platform?",
            "Question 8: How do I report a technical issue or bug?",
            "Question 9: Can I set up recurring payments for bills?",
            "Question 10: Where can I find user manuals and guides for using the software?"
        ]

        answers = [
            "To create a new account, navigate to the 'Account Management' section, click on 'Create Account,' and fill in the required information such as name, address, and initial deposit amount.",
            "Yes, you can edit your account information by accessing the 'Edit Account' feature under the 'Account Management' section. Simply select the account you wish to edit and update the relevant details.",
            "To deposit funds into your account, go to the 'Financial Transactions' section, choose the 'Deposit' option, enter the amount you wish to deposit, and follow the prompts to complete the transaction.",
            "To transfer money to another account, select the 'Fund Transfer' option in the 'Financial Transactions' section. Enter the recipient's account details and the amount you wish to transfer to complete the transaction.",
            "You can view your account balance by accessing the 'Account Summary' feature in the 'Account Services' section. It will display your current balance along with transaction history.",
            "If you forget your login credentials, click on the 'Forgot Password' link on the login page. Follow the instructions to reset your password securely.",
            "Yes, we prioritize the security of your personal information. Our platform uses encryption and follows strict security protocols to safeguard your data.",
            "To report a technical issue or bug, please navigate to the 'Helpdesk' section and select 'Report Issue.' Provide a detailed description of the problem you encountered, and our support team will investigate promptly.",
            "Yes, you can set up recurring payments for bills by accessing the 'Recurring Payments' feature in the 'Account Services' section. Enter the payment details and schedule, and the system will automatically process payments on your behalf.",
            "User manuals and guides are available in the 'Documentation' section. You can access them to learn more about using various features and functionalities of the banking software system."
        ]

        for question, answer in zip(questions, answers):
            button = QPushButton(question)
            self.layout.addWidget(button)
            self.question_buttons.append(button)
            
            answer_text = QTextEdit()
            answer_text.setReadOnly(True)
            answer_text.setPlainText(answer)
            answer_text.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            answer_text.hide()
            self.layout.addWidget(answer_text)
            self.answer_texts.append(answer_text)

            button.clicked.connect(lambda state, index=len(self.question_buttons)-1: self.toggle_answer(index))

        self.back_button = QPushButton("Back to Home")
        self.back_button.clicked.connect(self.go_back_to_main_menu)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)
       
    def toggle_answer(self, index):
        answer_text = self.answer_texts[index]
        if answer_text.isHidden():
            answer_text.show()
        else:
            answer_text.hide()
    def go_back_to_main_menu(self):
        self.go_back.emit()
        self.close()

if __name__ == "__main__":
    app = QApplication([])
    helpdesk_widget = HelpdeskWidget()
    helpdesk_widget.show()
    app.exec_()
