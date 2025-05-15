from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
from database.db_queries import fetch_users

class TeacherManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.teacher_list_widget = QTableWidget()
        layout.addWidget(self.teacher_list_widget)
        self.load_teacher_list()

    def load_teacher_list(self):
        users = fetch_users()
        if users:
            self.teacher_list_widget.setRowCount(len(users))
            self.teacher_list_widget.setColumnCount(len(users[0]))
            self.teacher_list_widget.setHorizontalHeaderLabels(["ID", "Username", "Password", "Created At"])
            for row_idx, row in enumerate(users):
                for col_idx, value in enumerate(row):
                    self.teacher_list_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        else:
            self.teacher_list_widget.setRowCount(0)
            self.teacher_list_widget.setColumnCount(0)
