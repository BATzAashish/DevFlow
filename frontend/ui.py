from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                            QSplitter, QScrollArea)
from PyQt5.QtCore import Qt
import sys

from .menu_interface import ExpandableMenu
from .chat_interface import ChatInterface

class UI(QWidget):
    def __init__(self, store):
        super().__init__()
        self.store = store
        self.init_ui()
    
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