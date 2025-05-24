from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout,
    QLineEdit, QFormLayout, QMessageBox
)
from database.db_queries import fetch_users, insert_user, update_user, delete_user

class UserEditDialog(QDialog):
    def __init__(self, parent=None, user_id=None, name="", email="", phone="", birthday=""):
        super().__init__(parent)
        self.setWindowTitle("Thêm/Sửa người dùng")
        self.setMinimumSize(400, 300)
        self.user_id = user_id
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self.name_edit = QLineEdit(name)
        self.email_edit = QLineEdit(email)
        self.phone_edit = QLineEdit(phone)
        self.birthday_edit = QLineEdit(birthday)
        form.addRow("Name:", self.name_edit)
        form.addRow("Email:", self.email_edit)
        form.addRow("Phone:", self.phone_edit)
        form.addRow("Birthday:", self.birthday_edit)
        layout.addLayout(form)
        self.save_button = QPushButton("Lưu")
        self.save_button.clicked.connect(self.save)
        layout.addWidget(self.save_button)

    def save(self):
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()
        phone = self.phone_edit.text().strip()
        birthday = self.birthday_edit.text().strip()
        if not name or not email:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng nhập đầy đủ tên và email.")
            return
        try:
            if self.user_id:
                update_user(self.user_id, name, email, phone, birthday)
            else:
                import hashlib
                password_hash = hashlib.sha256("123456".encode()).hexdigest()
                insert_user(name, email, phone, birthday, password_hash)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu: {e}")

class UserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quản lý người dùng")
        self.setMinimumSize(900, 500)
        layout = QVBoxLayout(self)

        # Nút chức năng
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Thêm")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        self.refresh_button = QPushButton("Làm mới")
        self.add_button.clicked.connect(self.add_user_dialog)
        self.edit_button.clicked.connect(self.edit_user_dialog)
        self.delete_button.clicked.connect(self.delete_user)
        self.refresh_button.clicked.connect(self.load_user_list)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.load_user_list()

    def load_user_list(self):
        users = fetch_users()
        self.table.setRowCount(len(users))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "Birthday", "Created At"])
        for row_idx, row in enumerate(users):
            for col_idx, value in enumerate(row):
                if col_idx == 5:  # Ẩn password_hash
                    continue
                display_col = col_idx if col_idx < 5 else col_idx - 1
                if display_col < 6:
                    self.table.setItem(row_idx, display_col, QTableWidgetItem(str(value)))

    def add_user_dialog(self):
        dlg = UserEditDialog(self)
        if dlg.exec():
            self.load_user_list()

    def edit_user_dialog(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chọn dòng", "Vui lòng chọn người dùng để sửa.")
            return
        user_id = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        email = self.table.item(row, 2).text()
        phone = self.table.item(row, 3).text()
        birthday = self.table.item(row, 4).text()
        dlg = UserEditDialog(self, user_id, name, email, phone, birthday)
        if dlg.exec():
            self.load_user_list()

    def delete_user(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chọn dòng", "Vui lòng chọn người dùng để xóa.")
            return
        user_id = self.table.item(row, 0).text()
        reply = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa người dùng ID {user_id}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_user(user_id)
                self.load_user_list()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa: {e}")
