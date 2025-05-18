from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton, 
                            QTextEdit, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt

class TechStackDialog(QDialog):
    def __init__(self, current_stack="", parent=None):
        super().__init__(parent)
        self.current_stack = current_stack
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Edit Tech Stack")
        self.setFixedSize(400, 300)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #121B22;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #00A884;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #008C74;
            }
            QTextEdit {
                background-color: #2A2F32;
                color: white;
                border: 1px solid #3A3F41;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 1px solid #00A884;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Instructions
        instruction_label = QLabel("Enter your desired tech stack (e.g., Python, PyQt5, C++):")
        layout.addWidget(instruction_label)
        
        # Text edit for tech stack
        self.tech_stack_edit = QTextEdit()
        self.tech_stack_edit.setPlaceholderText("Enter tech stack here...")
        self.tech_stack_edit.setText(self.current_stack)
        layout.addWidget(self.tech_stack_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.accept)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #2A2F32;
            }
            QPushButton:hover {
                background-color: #3A3F41;
            }
        """)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_tech_stack(self):
        return self.tech_stack_edit.toPlainText().strip()
