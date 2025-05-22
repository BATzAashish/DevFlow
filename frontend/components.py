from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard, QGuiApplication

class CodeSnippetWidget(QWidget):
    def __init__(self, title, code, parent=None):
        super().__init__(parent)
        self.code = code
        self.setup_ui(title)
    
    def setup_ui(self, title):
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        # Header with title and copy button
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(10, 5, 10, 5)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 13px;
            }
        """)
        header_layout.addWidget(title_label)
        
        copy_button = QPushButton("Copy")
        copy_button.setFixedSize(60, 25)
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: #404B53;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #515B63;
            }
        """)
        copy_button.clicked.connect(self.copy_code)
        header_layout.addWidget(copy_button)
        
        layout.addWidget(header)
        
        # Code content
        code_frame = QFrame()
        code_frame.setStyleSheet("""
            QFrame {
                background-color: #1E2428;
                border: 1px solid #3F3F41;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        code_layout = QVBoxLayout(code_frame)
        code_layout.setContentsMargins(10, 10, 10, 10)
        
        code_label = QLabel(self.code)
        code_label.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                font-family: "Consolas", "Monaco", "Courier New", monospace;
                font-size: 12px;
                line-height: 1.5;
            }
        """)
        code_label.setWordWrap(True)
        code_layout.addWidget(code_label)
        
        layout.addWidget(code_frame)
        
    def copy_code(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.code)
        
class CommandWidget(QWidget):
    def __init__(self, command, is_terminal=True, parent=None):
        super().__init__(parent)
        self.command = command
        self.setup_ui(is_terminal)
    
    def setup_ui(self, is_terminal):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 2, 0, 2)
        
        if is_terminal:
            # Command box with copy button
            cmd_container = QFrame()
            cmd_container.setStyleSheet("""
                QFrame {
                    background-color: #1E2428;
                    border: 1px solid #3F3F41;
                    border-radius: 4px;
                }
            """)
            cmd_layout = QHBoxLayout(cmd_container)
            cmd_layout.setContentsMargins(10, 5, 10, 5)
            
            cmd_label = QLabel(self.command)
            cmd_label.setStyleSheet("""
                QLabel {
                    color: #E0E0E0;
                    font-family: "Consolas", "Monaco", "Courier New", monospace;
                    font-size: 12px;
                }
            """)
            cmd_layout.addWidget(cmd_label)
            
            copy_button = QPushButton("Copy")
            copy_button.setFixedSize(60, 25)
            copy_button.setStyleSheet("""
                QPushButton {
                    background-color: #404B53;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #515B63;
                }
            """)
            copy_button.clicked.connect(self.copy_command)
            cmd_layout.addWidget(copy_button)
            
            layout.addWidget(cmd_container)
        else:
            # Regular text for general commands
            label = QLabel(self.command)
            label.setStyleSheet("""
                QLabel {
                    color: white;
                    font-size: 12px;
                }
            """)
            label.setWordWrap(True)
            layout.addWidget(label)
            
    def copy_command(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.command)
