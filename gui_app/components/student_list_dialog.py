from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import os
import glob

class StudentImageDialog(QDialog):
    def __init__(self, img_path):
        super().__init__()
        self.setWindowTitle("Xem ảnh sinh viên")
        self.setMinimumSize(400, 400)
        layout = QVBoxLayout(self)
        label = QLabel(self)
        pixmap = QPixmap(img_path)
        label.setPixmap(pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(label)

class StudentListDialog(QDialog):
    def __init__(self, faces_dir):
        super().__init__()
        self.setWindowTitle("Quản lý sinh viên (theo thư mục faces5)")
        self.setMinimumSize(900, 500)
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Chỉ cần nút làm mới
        button_layout = QHBoxLayout()
        self.refresh_button = QPushButton("Làm mới")
        self.refresh_button.clicked.connect(self.load_student_list)
        button_layout.addStretch(1)
        button_layout.addWidget(self.refresh_button)
        button_layout.addStretch(1)
        layout.addLayout(button_layout)

        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.faces_dir = faces_dir
        self.load_student_list()
        self.table.cellDoubleClicked.connect(self.show_image_dialog)

    def load_student_list(self):
        # Quét thư mục faces_dir, mỗi thư mục con là 1 sinh viên, mỗi file ảnh là 1 khuôn mặt
        image_paths = glob.glob(os.path.join(self.faces_dir, "*", "*.jpg")) + glob.glob(os.path.join(self.faces_dir, "*", "*.png"))
        data = []
        for img_path in image_paths:
            label = os.path.basename(os.path.dirname(img_path))
            filename = os.path.basename(img_path)
            data.append((label, filename, img_path))
        self.table.setRowCount(len(data))
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Tên sinh viên (folder)", "Tên file ảnh", "Đường dẫn ảnh"])
        for row_idx, (label, filename, img_path) in enumerate(data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(label))
            self.table.setItem(row_idx, 1, QTableWidgetItem(filename))
            self.table.setItem(row_idx, 2, QTableWidgetItem(img_path))

    def show_image_dialog(self, row, column):
        img_path = self.table.item(row, 2).text()
        dlg = StudentImageDialog(img_path)
        dlg.exec()
