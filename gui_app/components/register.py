from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from database.db_queries import insert_user

class RegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
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

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "All fields are required!")
            return

        try:
            insert_user(username, password)
            QMessageBox.information(self, "Success", "User registered successfully!")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to register user: {e}")