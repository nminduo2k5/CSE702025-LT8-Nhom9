from PyQt6.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QMessageBox
import pandas as pd

class CSVViewer(QDialog):
    def __init__(self, csv_path):
        super().__init__()
        self.setWindowTitle("CSV Viewer")
        self.setGeometry(200, 200, 800, 600)
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
