from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem
# ...existing code...

class UserManagementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Quản lý người dùng")
        self.setMinimumSize(700, 500)
        layout = QVBoxLayout(self)
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.load_user_list()

    def load_user_list(self):
        # Hiển thị dữ liệu mẫu như yêu cầu
        users = [
            (1, "Messi", "123", "2025-05-04 05:41:39")
        ]
        self.table.setRowCount(len(users))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email", "Created At"])
        for row_idx, row in enumerate(users):
            for col_idx, value in enumerate(row):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
