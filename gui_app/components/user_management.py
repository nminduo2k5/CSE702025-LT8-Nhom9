from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from database.db_queries import fetch_users

class UserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quản lý người dùng")
        self.setMinimumSize(900, 500)
        layout = QVBoxLayout(self)

        # Thêm nút làm mới
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Làm mới danh sách")
        self.refresh_button.clicked.connect(self.load_user_list)
        button_layout.addStretch(1)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.load_user_list()

    def load_user_list(self):
        users = fetch_users()
        # users: (id, name, email, phone, birthday, password_hash, created_at)
        self.table.setRowCount(len(users))
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Phone", "Birthday", "Created At"])
        for row_idx, row in enumerate(users):
            for col_idx, value in enumerate(row):
                # Ẩn password_hash khỏi giao diện
                if col_idx == 5:
                    continue
                # Điều chỉnh chỉ số cột khi bỏ qua password_hash
                display_col = col_idx if col_idx < 5 else col_idx - 1
                if display_col < 6:
                    self.table.setItem(row_idx, display_col, QTableWidgetItem(str(value)))
