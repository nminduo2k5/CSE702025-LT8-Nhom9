from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QDialog, QFormLayout, QLineEdit, QMessageBox
from database.db_queries import fetch_users, insert_user, update_user, delete_user
import os
import glob

class StudentManagementWidget(QWidget):
    def __init__(self, faces_dir):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Nút chức năng
        button_layout = QHBoxLayout()
        self.add_button = QPushButton("Thêm")
        self.edit_button = QPushButton("Sửa")
        self.delete_button = QPushButton("Xóa")
        self.refresh_button = QPushButton("Làm mới")
        self.add_button.clicked.connect(self.add_student_dialog)
        self.edit_button.clicked.connect(self.edit_student_dialog)
        self.delete_button.clicked.connect(self.delete_student)
        self.refresh_button.clicked.connect(self.load_student_list)
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch(1)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)

        self.student_list_widget = QTableWidget()
        layout.addWidget(self.student_list_widget)
        self.faces_dir = faces_dir
        self.load_student_list()

    def load_student_list(self):
        users = fetch_users()
        self.student_list_widget.setRowCount(len(users))
        self.student_list_widget.setColumnCount(6)
        self.student_list_widget.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "Birthday", "Created At"])
        for row_idx, row in enumerate(users):
            for col_idx, value in enumerate(row):
                if col_idx == 5:
                    continue
                display_col = col_idx if col_idx < 5 else col_idx - 1
                if display_col < 6:
                    self.student_list_widget.setItem(row_idx, display_col, QTableWidgetItem(str(value)))

    def add_student_dialog(self):
        dlg = StudentEditDialog(self)
        if dlg.exec():
            self.load_student_list()

    def edit_student_dialog(self):
        row = self.student_list_widget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chọn dòng", "Vui lòng chọn sinh viên để sửa.")
            return
        user_id = self.student_list_widget.item(row, 0).text()
        name = self.student_list_widget.item(row, 1).text()
        email = self.student_list_widget.item(row, 2).text()
        phone = self.student_list_widget.item(row, 3).text()
        birthday = self.student_list_widget.item(row, 4).text()
        dlg = StudentEditDialog(self, user_id, name, email, phone, birthday)
        if dlg.exec():
            self.load_student_list()

    def delete_student(self):
        row = self.student_list_widget.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Chọn dòng", "Vui lòng chọn sinh viên để xóa.")
            return
        user_id = self.student_list_widget.item(row, 0).text()
        reply = QMessageBox.question(self, "Xác nhận", f"Bạn có chắc muốn xóa sinh viên ID {user_id}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                delete_user(user_id)
                self.load_student_list()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa: {e}")

class StudentEditDialog(QDialog):
    def __init__(self, parent=None, user_id=None, name="", email="", phone="", birthday=""):
        super().__init__(parent)
        self.setWindowTitle("Thêm/Sửa sinh viên")
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
