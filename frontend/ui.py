from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QSplitter, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt
import sys
import os

from .menu_interface import ExpandableMenu
from .chat_interface import ChatInterface
from .project_setup import ProjectSetupDialog

class UI(QWidget):
    def __init__(self, store):
        super().__init__()
        self.store = store
        
        # Show project setup dialog
        dialog = ProjectSetupDialog(self)
        dialog.setFixedSize(500, 450)  # Set a reasonable size for the dialog
        result = dialog.exec_()
        
        if result == ProjectSetupDialog.Accepted:
            project_info = dialog.get_project_info()
            # Create project directory if it doesn't exist
            project_path = os.path.join(project_info['location'], project_info['name'])
            try:
                os.makedirs(project_path, exist_ok=True)
                self.project_path = project_path
                self.project_name = project_info['name']
                self.project_description = project_info['description']
                QMessageBox.information(
                    self,
                    "Success",
                    f"Project folder created successfully at:\n{project_path}"
                )
                self.init_ui()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create project directory: {str(e)}")
                sys.exit(1)
        else:
            sys.exit(0)
    
    def init_ui(self):
        self.setWindowTitle("DevFlow")
        self.showMaximized()

        layout = QVBoxLayout()
        
        # Create main horizontal splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Add expandable menu to left side
        menu_scroll = QScrollArea()
        menu_scroll.setWidget(ExpandableMenu())
        menu_scroll.setWidgetResizable(True)
        
        # Set width for menu container (2/3 of screen width)
        screen = QApplication.primaryScreen().size()
        menu_width = int(screen.width() * 0.67)  # 67% of screen width
        menu_scroll.setMinimumWidth(menu_width)
        menu_scroll.setMaximumWidth(menu_width)
        menu_scroll.setStyleSheet("QScrollArea { border: none; background-color: #121B22; }")
        splitter.addWidget(menu_scroll)
        
        # Create and add chat interface
        chat_interface = ChatInterface(self.store)
        
        # Set width for chat container (1/3 of screen width)
        chat_width = int(screen.width() * 0.3)  # 33% of screen width
        chat_interface.setMinimumWidth(chat_width)
        chat_interface.setMaximumWidth(chat_width)
        
        # Add chat interface to splitter
        splitter.addWidget(chat_interface)
        
        # Add splitter to main layout
        layout.addWidget(splitter)
        self.setLayout(layout)

        # Apply window background
        self.setStyleSheet("background-color: #121B22;")

def run_app(store):
    app = QApplication([])
    window = UI(store)
    window.show()
    sys.exit(app.exec_())