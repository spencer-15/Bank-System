from PyQt5.QtCore import pyqtSignal

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
