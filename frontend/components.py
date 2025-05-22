from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QClipboard, QGuiApplication

class CodeSnippetWidget(QWidget):
    def __init__(self, code, parent=None):
        super().__init__(parent)
        self.code = code
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Code content container
        code_frame = QFrame()
        code_frame.setStyleSheet("""
            QFrame {
                background-color: #1E1E1E;
                border: none;
                border-radius: 6px;
            }
        """)
        
        # Main horizontal layout for code and copy button
        code_layout = QHBoxLayout(code_frame)
        code_layout.setContentsMargins(15, 12, 12, 12)
        code_layout.setSpacing(15)
        
        # Code text with proper styling
        code_label = QLabel(self.code)
        code_label.setStyleSheet("""
            QLabel {
                color: #E0E0E0;
                font-family: "Consolas", "Monaco", "Courier New", monospace;
                font-size: 13px;
                line-height: 1.6;
                letter-spacing: 0.3px;
            }
        """)
        code_label.setWordWrap(True)
        code_layout.addWidget(code_label, stretch=1)
        
        # Copy button with improved styling
        copy_button = QPushButton("📋 Copy")
        copy_button.setFixedSize(100, 28)  # Increased width from 80 to 100
        copy_button.setStyleSheet("""
            QPushButton {
                background-color: #2D3439;
                color: #E0E0E0;
                border: 1px solid #404B53;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 13px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #404B53;
                border-color: #515B63;
            }
        """)
        copy_button.clicked.connect(self.copy_code)
        code_layout.addWidget(copy_button, alignment=Qt.AlignTop)
        
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
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        if is_terminal:
            # Terminal command container
            cmd_frame = QFrame()
            cmd_frame.setStyleSheet("""
                QFrame {
                    background-color: #1E1E1E;
                    border: none;
                    border-radius: 6px;
                }
            """)
            
            # Main horizontal layout
            cmd_layout = QHBoxLayout(cmd_frame)
            cmd_layout.setContentsMargins(15, 12, 12, 12)
            cmd_layout.setSpacing(15)
            
            # Command text with icon
            cmd_text = f"$ {self.command}"
            cmd_label = QLabel(cmd_text)
            cmd_label.setStyleSheet("""
                QLabel {
                    color: #E0E0E0;
                    font-family: "Consolas", "Monaco", "Courier New", monospace;
                    font-size: 13px;
                    line-height: 1.6;
                    letter-spacing: 0.3px;
                }
            """)
            cmd_label.setWordWrap(True)
            cmd_layout.addWidget(cmd_label, stretch=1)
            
            # Copy button with improved styling
            copy_button = QPushButton("📋 Copy")
            copy_button.setFixedSize(100, 28)  # Increased width from 80 to 100
            copy_button.setStyleSheet("""
                QPushButton {
                    background-color: #2D3439;
                    color: #E0E0E0;
                    border: 1px solid #404B53;
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-size: 13px;
                    min-width: 100px;
                }
                QPushButton:hover {
                    background-color: #404B53;
                    border-color: #515B63;
                }
            """)
            copy_button.clicked.connect(self.copy_command)
            cmd_layout.addWidget(copy_button, alignment=Qt.AlignTop)
            
            layout.addWidget(cmd_frame)
        else:
            # Regular command text (not in a terminal box)
            label = QLabel(self.command)
            label.setStyleSheet("""
                QLabel {
                    color: #E0E0E0;
                    font-size: 14px;
                    line-height: 1.4;
                    padding-left: 15px;
                    letter-spacing: 0.3px;
                }
            """)
            label.setWordWrap(True)
            layout.addWidget(label)
            
    def copy_command(self):
        clipboard = QGuiApplication.clipboard()
        clipboard.setText(self.command)
