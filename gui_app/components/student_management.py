from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
import os
import glob

class StudentManagementWidget(QWidget):
    def __init__(self, faces_dir):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.student_list_widget = QTableWidget()
        layout.addWidget(self.student_list_widget)
        self.faces_dir = faces_dir
        self.load_student_list()

    def load_student_list(self):
        image_paths = glob.glob(os.path.join(self.faces_dir, "*", "*.jpg")) + glob.glob(os.path.join(self.faces_dir, "*", "*.png"))
        data = []
        for img_path in image_paths:
            label = os.path.basename(os.path.dirname(img_path))
            filename = os.path.basename(img_path)
            data.append((filename, label, img_path))
        self.student_list_widget.setRowCount(len(data))
        self.student_list_widget.setColumnCount(3)
        self.student_list_widget.setHorizontalHeaderLabels(["Ảnh", "Nhãn", "Đường dẫn"])
        for row_idx, (filename, label, img_path) in enumerate(data):
            self.student_list_widget.setItem(row_idx, 0, QTableWidgetItem(filename))
            self.student_list_widget.setItem(row_idx, 1, QTableWidgetItem(label))
            self.student_list_widget.setItem(row_idx, 2, QTableWidgetItem(img_path))
