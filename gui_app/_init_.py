1# gui_app/__init__.py
from .app_gui import AppGUI  # Tự động export class AppGUI khi import package

__all__ = ["AppGUI"]  # Danh sách các thành phần được phép import