from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QMessageBox, QVBoxLayout, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import pandas as pd
import os

class CSVViewer(QDialog):
    def __init__(self, csv_path):
        super().__init__()
        self.setWindowTitle("CSV Viewer")
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout(self)
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)
        self.csv_path = csv_path
        self.load_csv(csv_path)
        self.table_widget.cellDoubleClicked.connect(self.show_face_image)

    def load_csv(self, csv_path):
        try:
            data = pd.read_csv(csv_path)
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(len(data.columns))
            self.table_widget.setHorizontalHeaderLabels(list(data.columns))
            for row_idx, row in enumerate(data.itertuples(index=False)):
                for col_idx, value in enumerate(row):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV file: {e}")

    def show_face_image(self, row, column):
        # Lấy tên sinh viên từ cột "Name"
        name_item = self.table_widget.item(row, 0)
        if not name_item:
            return
        name = name_item.text()
        # Không hiển thị ảnh cho dòng tổng kết
        if name.upper() == "SUMMARY" or name == "Unknown":
            return

        # Tìm đường dẫn ảnh khuôn mặt trong thư mục faces_dir
        # Giả định cấu trúc: faces_dir/<name>/<*.jpg|*.png>
        # Lấy faces_dir từ biến môi trường hoặc cấu hình toàn cục
        from c.cConst import Const
        faces_dir = Const().faces_dir
        import glob
        image_paths = glob.glob(os.path.join(faces_dir, name, "*.jpg")) + glob.glob(os.path.join(faces_dir, name, "*.png"))
        if not image_paths:
            QMessageBox.information(self, "No Image", f"No image found for {name}")
            return

        # Hiển thị ảnh đầu tiên tìm được
        img_path = image_paths[0]
        dlg = QDialog(self)
        dlg.setWindowTitle(f"Ảnh của {name}")
        dlg.setMinimumSize(400, 400)
        vbox = QVBoxLayout(dlg)
        label = QTableWidgetItem()
        label_widget = QLabel()
        pixmap = QPixmap(img_path)
        label_widget.setPixmap(pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        vbox.addWidget(label_widget)
        dlg.exec()
