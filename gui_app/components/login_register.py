from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QStackedWidget, QWidget, QLabel, QLineEdit, QFormLayout, QHBoxLayout, QMessageBox
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
import hashlib
from database.db_queries import insert_user, fetch_users

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

        self.register_birthday = QLineEdit()
        self.register_birthday.setPlaceholderText("YYYY-MM-DD")
        form_layout.addRow("Birthday:", self.register_birthday)

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
        username = self.login_username.text().strip()
        password = self.login_password.text()
        if not username or not password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        users = fetch_users()
        # users: [(id, name, email, phone, birthday, password_hash, created_at), ...]
        for user in users:
            if username == user[1] and password_hash == user[5]:
                self.accept()
                return
        QMessageBox.warning(self, "Lỗi", "Sai tên đăng nhập hoặc mật khẩu.")

    def handle_register(self):
        username = self.register_username.text().strip()
        email = self.register_email.text().strip()
        phone = self.register_phone.text().strip()
        birthday = self.register_birthday.text().strip()
        password = self.register_password.text()
        confirm_password = self.register_confirm_password.text()
        if not username or not email or not phone or not birthday or not password or not confirm_password:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin.")
            return
        if password != confirm_password:
            QMessageBox.warning(self, "Lỗi", "Mật khẩu không khớp.")
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        try:
            insert_user(username, email, phone, birthday, password_hash)
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Bạn có thể đăng nhập.")
            self.show_login_page()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Đăng ký thất bại: {e}")