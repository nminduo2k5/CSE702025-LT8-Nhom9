from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QStackedWidget, QWidget, QLabel, QLineEdit, QFormLayout, QHBoxLayout
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

class LoginRegisterWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phenikaa Attendance System")
        self.setFixedSize(400, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Add a logo or banner
        logo_label = QLabel()
        pixmap = QPixmap("path_to_logo.png")  # Replace with the path to your logo
        logo_label.setPixmap(pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(logo_label)

        # Title
        title_label = QLabel("Facial Attendance System")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)

        # Stacked widget for login and register
        self.stacked_widget = QStackedWidget()
        self.login_page = self.create_login_page()
        self.register_page = self.create_register_page()
        self.stacked_widget.addWidget(self.login_page)
        self.stacked_widget.addWidget(self.register_page)
        main_layout.addWidget(self.stacked_widget)

        self.setLayout(main_layout)

    def create_login_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Login form
        form_layout = QFormLayout()
        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        form_layout.addRow("Username:", self.login_username)

        self.login_password = QLineEdit()
        self.login_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.login_password.setPlaceholderText("Enter your password")
        form_layout.addRow("Password:", self.login_password)

        layout.addLayout(form_layout)

        # Login button
        login_button = QPushButton("Login")
        login_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")
        login_button.clicked.connect(self.handle_login)
        layout.addWidget(login_button)

        # Switch to register button
        switch_to_register_button = QPushButton("Don't have an account? Register")
        switch_to_register_button.setStyleSheet("color: blue; text-decoration: underline;")
        switch_to_register_button.clicked.connect(self.show_register_page)
        layout.addWidget(switch_to_register_button, alignment=Qt.AlignmentFlag.AlignCenter)

        page.setLayout(layout)
        return page

    def create_register_page(self):
        page = QWidget()
        layout = QVBoxLayout()

        # Register form
        form_layout = QFormLayout()
        self.register_username = QLineEdit()
        self.register_username.setPlaceholderText("Enter your username")
        form_layout.addRow("Username:", self.register_username)

        self.register_email = QLineEdit()
        self.register_email.setPlaceholderText("Enter your email")
        form_layout.addRow("Email:", self.register_email)

        self.register_phone = QLineEdit()
        self.register_phone.setPlaceholderText("Enter your phone number")
        form_layout.addRow("Phone Number:", self.register_phone)

        self.register_password = QLineEdit()
        self.register_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_password.setPlaceholderText("Enter your password")
        form_layout.addRow("Password:", self.register_password)

        self.register_confirm_password = QLineEdit()
        self.register_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.register_confirm_password.setPlaceholderText("Confirm your password")
        form_layout.addRow("Confirm Password:", self.register_confirm_password)

        layout.addLayout(form_layout)

        # Register button
        register_button = QPushButton("Register")
        register_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px; font-size: 14px;")
        register_button.clicked.connect(self.handle_register)
        layout.addWidget(register_button)

        # Switch to login button
        switch_to_login_button = QPushButton("Already have an account? Login")
        switch_to_login_button.setStyleSheet("color: blue; text-decoration: underline;")
        switch_to_login_button.clicked.connect(self.show_login_page)
        layout.addWidget(switch_to_login_button, alignment=Qt.AlignmentFlag.AlignCenter)

        page.setLayout(layout)
        return page

    def show_login_page(self):
        self.stacked_widget.setCurrentWidget(self.login_page)

    def show_register_page(self):
        self.stacked_widget.setCurrentWidget(self.register_page)

    def handle_login(self):
        username = self.login_username.text()
        password = self.login_password.text()
        # Add login logic here
        print(f"Logging in with {username} and {password}")
        self.accept()

    def handle_register(self):
        username = self.register_username.text()
        email = self.register_email.text()
        phone = self.register_phone.text()
        password = self.register_password.text()
        confirm_password = self.register_confirm_password.text()
        if password != confirm_password:
            print("Passwords do not match!")
            return
        # Add register logic here
        print(f"Registering {username} with email {email}, phone {phone}, and password {password}")
        self.accept()