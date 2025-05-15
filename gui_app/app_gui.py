from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMenuBar, QToolBar, QStatusBar, QFileDialog, QMessageBox, QDialog, QLineEdit, QPushButton, QHBoxLayout, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt
import os
import cv2
import random
import pandas as pd
import glob
from load_model import load_model
from service.processing import build_targets
from service.frame_processor import frame_processor
from c.cConst import Const
from database.db_queries import create_users_table, insert_statistics_from_csv, fetch_users
from gui_app.components.login_register import LoginRegisterWindow

class CSVViewer(QDialog):
    def __init__(self, csv_path):
        super().__init__()
        self.setWindowTitle("CSV Viewer")
        self.setGeometry(200, 200, 800, 600)

        # Table widget to display CSV content
        self.table_widget = QTableWidget(self)
        self.table_widget.setGeometry(10, 10, 780, 580)

        self.load_csv(csv_path)

    def load_csv(self, csv_path):
        try:
            data = pd.read_csv(csv_path)
            self.table_widget.setRowCount(len(data))
            self.table_widget.setColumnCount(len(data.columns))
            self.table_widget.setHorizontalHeaderLabels(data.columns)

            for row_idx, row in data.iterrows():
                for col_idx, value in enumerate(row):
                    self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load CSV file: {e}")

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
        self.data = data  # Lưu lại để dùng khi click
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

class AppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phenikaa Attendance System")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize constants
        self.var = Const()
        self.detector, self.recognizer = load_model()
        self.targets = build_targets(self.detector, self.recognizer, self.var.faces_dir)
        self.colors = {name: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
                       for _, name in self.targets}

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Image viewer placeholder
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #4CAF50; padding: 10px;")
        self.layout.addWidget(self.image_label)

        # Add a horizontal layout for buttons (all buttons in one row)
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        # Add "Process Image" button
        self.process_image_button = QPushButton("Process Image")
        self.process_image_button.clicked.connect(self.process_image)
        self.button_layout.addWidget(self.process_image_button)

        # Add "View CSV" button
        self.view_csv_button = QPushButton("View CSV")
        self.view_csv_button.setEnabled(False)
        self.view_csv_button.clicked.connect(self.view_csv_file)
        self.button_layout.addWidget(self.view_csv_button)

        # Add "Quản lý sinh viên" button
        self.view_students_button = QPushButton("Quản lý sinh viên")
        self.view_students_button.clicked.connect(self.show_student_management)
        self.button_layout.addWidget(self.view_students_button)

        # Menu bar
        self.menu_bar = QMenuBar()
        self.setMenuBar(self.menu_bar)
        file_menu = self.menu_bar.addMenu("File")
        open_action = QAction("Open Image", self)
        open_action.triggered.connect(self.process_image)
        file_menu.addAction(open_action)

        # Tool bar
        self.tool_bar = QToolBar()
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.tool_bar)
        process_action = QAction("Process Image", self)
        process_action.triggered.connect(self.process_image)
        self.tool_bar.addAction(process_action)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    def process_image(self):
        if not self.detector or not self.recognizer or not self.targets:
            QMessageBox.warning(self, "Warning", "Models and targets are still loading. Please wait.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select an Image", "", "Image Files (*.jpg *.png)")
        if not file_path:
            return

        try:
            self.status_bar.showMessage("Processing image...")

            img = cv2.imread(file_path)
            detected_faces = []  # List to store detection results
            processed_img = frame_processor(
                img, self.detector, self.recognizer, self.targets, 
                self.colors, self.var, detected_faces=detected_faces
            )

            # Save and display the processed image
            output_path = os.path.join(self.var.output_images_dir, f"processed_{os.path.basename(file_path)}")
            os.makedirs(self.var.output_images_dir, exist_ok=True)
            cv2.imwrite(output_path, processed_img)

            pixmap = QPixmap(output_path)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            ))
            self.status_bar.showMessage(f"Processed image saved to {output_path}")

            # Generate and save statistics CSV
            if detected_faces:
                csv_filename = f"statistics_{os.path.basename(file_path).split('.')[0]}.csv"
                csv_path = os.path.join(self.var.output_images_dir, csv_filename)
                self.generate_csv_from_faces(detected_faces, self.var.output_images_dir, csv_filename)

                # Insert statistics into the database
                insert_statistics_from_csv(csv_path)

                # Verify if the CSV file exists before enabling the button
                if os.path.exists(csv_path):
                    self.csv_path = csv_path
                    self.view_csv_button.setEnabled(True)
                else:
                    self.view_csv_button.setEnabled(False)
                    QMessageBox.warning(self, "Warning", "CSV file could not be created.")

                QMessageBox.information(self, "Success", f"Statistics saved to {csv_path} and database updated.")
            else:
                self.view_csv_button.setEnabled(False)
                QMessageBox.warning(self, "Warning", "No faces detected in the image.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process image: {e}")

    def view_csv_file(self):
        if hasattr(self, 'csv_path') and os.path.exists(self.csv_path):
            try:
                csv_viewer = CSVViewer(self.csv_path)
                csv_viewer.exec()  # Show the CSV viewer dialog
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open CSV viewer: {e}")
        else:
            QMessageBox.warning(self, "Warning", "No CSV file available to view or file not found.")

    def generate_csv_from_faces(self, detected_faces, output_directory, filename):
        if not detected_faces:
            print("No detected faces to save.")
            return

        df_faces = pd.DataFrame(detected_faces, columns=["Name", "Confidence"])

        total_faces = len(detected_faces)
        recognized_faces = sum(1 for face in detected_faces if face["Name"] != "Unknown")
        recognition_rate = (recognized_faces / total_faces) * 100 if total_faces > 0 else 0

        summary_data = {
            "Name": ["Summary"],
            "Confidence": [""],
            "Total Faces": [total_faces],
            "Recognized Faces": [recognized_faces],
            "Recognition Rate (%)": [recognition_rate]
        }
        df_summary = pd.DataFrame(summary_data)

        df_faces = pd.concat([df_faces, df_summary], ignore_index=True)

        csv_path = os.path.join(output_directory, filename)
        df_faces.to_csv(csv_path, index=False)
        print(f"Statistics saved to: {csv_path}")

    def show_student_management(self):
        dlg = StudentListDialog(self.var.faces_dir)
        dlg.exec()

if __name__ == "__main__":
    app = QApplication([])

    # Ensure the users table exists
    create_users_table()

    # Show login/register window
    login_register_window = LoginRegisterWindow()
    if login_register_window.exec() == QDialog.DialogCode.Accepted:
        window = AppGUI()
        window.show()
        app.exec()