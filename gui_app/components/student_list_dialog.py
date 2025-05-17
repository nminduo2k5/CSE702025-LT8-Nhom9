from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
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
        self.setWindowTitle("Quản lý sinh viên")
        self.setMinimumSize(700, 500)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.table = QTableWidget()
        layout.addWidget(self.table)
        image_paths = glob.glob(os.path.join(faces_dir, "*", "*.jpg")) + glob.glob(os.path.join(faces_dir, "*", "*.png"))
        data = []
        for img_path in image_paths:
            label = os.path.basename(os.path.dirname(img_path))
            filename = os.path.basename(img_path)
            data.append((filename, label, img_path))
        self.data = data
        self.table.setRowCount(len(data))
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Ảnh", "Nhãn"])
        for row_idx, (filename, label, img_path) in enumerate(data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(filename))
            self.table.setItem(row_idx, 1, QTableWidgetItem(label))
        self.table.cellDoubleClicked.connect(self.show_image_dialog)

    def show_image_dialog(self, row, column):
        img_path = self.data[row][2]
        dlg = StudentImageDialog(img_path)
        dlg.exec()
