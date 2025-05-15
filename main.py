from gui_app.app_gui import AppGUI
from database.db_queries import create_users_table
from PyQt6.QtWidgets import QApplication, QDialog
from gui_app.components.login_register import LoginRegisterWindow

def initialize_database():
    """
    Initialize the database by creating necessary tables.
    """
    create_users_table()

def main():
    initialize_database()
    app = QApplication([])

    # Show login/register window
    while True:
        login_register_window = LoginRegisterWindow()
        if login_register_window.exec() == QDialog.DialogCode.Accepted:
            break

    # Launch main application
    window = AppGUI()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()