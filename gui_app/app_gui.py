from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QMenuBar, QToolBar, QStatusBar,
    QFileDialog, QMessageBox, QPushButton, QHBoxLayout, QDialog
)
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtCore import Qt
import os
import cv2
import random
from load_model import load_model
from service.processing import build_targets
from service.frame_processor import frame_processor
from c.cConst import Const
from database.db_queries import create_users_table, create_attendance_table, insert_attendance_from_csv
from gui_app.components.login_register import LoginRegisterWindow
from gui_app.components.csv_viewer import CSVViewer
from gui_app.components.student_list_dialog import StudentListDialog  # Đã tách ra file riêng
from gui_app.logic.csv_logic import generate_csv_from_faces  # Đã tách ra file riêng
from gui_app.components.user_management import UserManagementDialog  # Đảm bảo đã import

class AppGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Phenikaa Attendance System")
        self.setGeometry(100, 100, 1200, 800)

        # Set main window background color and font
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f6fa;
            }
        """)

        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Title label (smaller)
        self.title_label = QLabel("PHENIKAA ATTENDANCE SYSTEM")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #273c75;
            margin-top: 18px;
            margin-bottom: 4px;
            letter-spacing: 2px;
        """)
        self.layout.addWidget(self.title_label)

        # Subtitle label
        self.subtitle_label = QLabel("Smart Face Recognition for Attendance")
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setStyleSheet("""
            font-size: 15px;
            color: #353b48;
            margin-bottom: 10px;
        """)
        self.layout.addWidget(self.subtitle_label)

        # Image viewer placeholder (bigger)
        self.image_label = QLabel("No image loaded")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("""
            border: 2px solid #4CAF50;
            padding: 10px;
            background-color: #fff;
            min-height: 500px;
            font-size: 20px;
            color: #718093;
        """)
        self.layout.addWidget(self.image_label, stretch=2)

        # Add a horizontal layout for buttons (all buttons in one row)
        self.button_layout = QHBoxLayout()
        self.layout.addLayout(self.button_layout)

        # Style for buttons
        button_style = """
            QPushButton {
                background-color: #273c75;
                color: white;
                border-radius: 8px;
                padding: 12px 28px;
                font-size: 16px;
                font-weight: bold;
                margin: 0 10px;
            }
            QPushButton:hover {
                background-color: #4cd137;
                color: #222;
            }
        """

        # Add "Process Image" button
        self.process_image_button = QPushButton("Process Image")
        self.process_image_button.setStyleSheet(button_style)
        self.process_image_button.clicked.connect(self.process_image)
        self.button_layout.addWidget(self.process_image_button)

        # Add "View CSV" button
        self.view_csv_button = QPushButton("View CSV")
        self.view_csv_button.setStyleSheet(button_style)
        self.view_csv_button.setEnabled(False)
        self.view_csv_button.clicked.connect(self.view_csv_file)
        self.button_layout.addWidget(self.view_csv_button)

        # Add "Quản lý sinh viên" button
        self.view_students_button = QPushButton("Quản lý sinh viên")
        self.view_students_button.setStyleSheet(button_style)
        self.view_students_button.clicked.connect(self.show_student_management)
        self.button_layout.addWidget(self.view_students_button)

        # Add "Quản lý người dùng" button
        self.view_users_button = QPushButton("Quản lý người dùng")
        self.view_users_button.setStyleSheet(button_style)
        self.view_users_button.clicked.connect(self.show_user_management)
        self.button_layout.addWidget(self.view_users_button)

        # Add stretch to center buttons
        self.button_layout.insertStretch(0, 1)
        self.button_layout.addStretch(1)

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
        self.status_bar.setStyleSheet("color: #0097e6; font-size: 14px;")
        self.status_bar.showMessage("Ready")

        # Initialize constants
        self.var = Const()
        self.detector, self.recognizer = load_model()
        self.targets = build_targets(self.detector, self.recognizer, self.var.faces_dir)
        self.colors = {name: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) 
                       for _, name in self.targets}

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

            # Generate and save attendance CSV
            if detected_faces:
                csv_filename = f"attendance_{os.path.basename(file_path).split('.')[0]}.csv"
                csv_path = os.path.join(self.var.output_images_dir, csv_filename)
                generate_csv_from_faces(detected_faces, self.var.output_images_dir, csv_filename)

                # Insert attendance into the database
                insert_attendance_from_csv(csv_path)

                # Verify if the CSV file exists before enabling the button
                if os.path.exists(csv_path):
                    self.csv_path = csv_path
                    self.view_csv_button.setEnabled(True)
                else:
                    self.view_csv_button.setEnabled(False)
                    QMessageBox.warning(self, "Warning", "CSV file could not be created.")

                QMessageBox.information(self, "Success", f"Attendance saved to {csv_path} and database updated.")
            else:
                self.view_csv_button.setEnabled(False)
                QMessageBox.warning(self, "Warning", "No faces detected in the image.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process image: {e}")

    def view_csv_file(self):
        if hasattr(self, 'csv_path') and os.path.exists(self.csv_path):
            try:
                csv_viewer = CSVViewer(self.csv_path)
                csv_viewer.exec()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open CSV viewer: {e}")
        else:
            QMessageBox.warning(self, "Warning", "No CSV file available to view or file not found.")

    def show_student_management(self):
        dlg = StudentListDialog(self.var.faces_dir)
        dlg.exec()

    def show_user_management(self):
        dlg = UserManagementDialog(self)
        dlg.exec()

if __name__ == "__main__":
    app = QApplication([])

    # Ensure the users and attendance tables exist
    create_users_table()
    create_attendance_table()

    # Show login/register window
    login_register_window = LoginRegisterWindow()
    if login_register_window.exec() == QDialog.DialogCode.Accepted:
        window = AppGUI()
        window.show()
        app.exec()