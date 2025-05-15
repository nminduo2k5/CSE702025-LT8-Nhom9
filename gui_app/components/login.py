from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database.db_queries import fetch_users

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.login_user)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        users = fetch_users()
        for user in users:
            if user[1] == username and user[2] == password:
                QMessageBox.information(self, "Success", "Login successful!")
                self.accept()
                return

        QMessageBox.critical(self, "Error", "Invalid username or password!")