from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QLineEdit, QFrame)
from PyQt5.QtCore import Qt
import os
from dotenv import load_dotenv

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Settings")
        self.setFixedSize(500, 300)
        
        # Apply styling
        self.setStyleSheet("""
            QDialog {
                background-color: #121B22;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLabel[heading=true] {
                color: #00A884;
                font-size: 18px;
                font-weight: bold;
                padding: 10px 0;
            }
            QLineEdit {
                background-color: #2A2F32;
                color: white;
                border: 1px solid #3A3F41;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #00A884;
            }
            QPushButton {
                background-color: #00A884;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #008C74;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 20, 30, 30)
        
        # API Settings Section
        api_heading = QLabel("API Settings")
        api_heading.setProperty("heading", True)
        layout.addWidget(api_heading)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #2A353F;")
        layout.addWidget(separator)
        
        # Gemini API Key
        api_container = QHBoxLayout()
        api_container.setSpacing(10)
        
        api_label = QLabel("Gemini API Key:")
        api_container.addWidget(api_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.Password)  # Hide API key
        api_container.addWidget(self.api_key_input, stretch=1)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_api_key)
        api_container.addWidget(save_button)
        
        layout.addLayout(api_container)
        
        # Load existing API key if it exists
        load_dotenv()
        existing_key = os.getenv("GEMINI_API_KEY", "")
        self.api_key_input.setText(existing_key)
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        self.setLayout(layout)
    
    def save_api_key(self):
        api_key = self.api_key_input.text().strip()
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        
        try:
            # Read existing .env content, preserving all non-GEMINI_API_KEY entries
            existing_content = []
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    for line in f:
                        # Skip empty lines and any variation of GEMINI_API_KEY
                        line = line.strip()
                        if line and not any(line.startswith(key) for key in ['GEMINI_API_KEY=', 'GEMINI_API_KEY ="', 'GEMINI_API_KEY="']):
                            existing_content.append(line)
            
            # Add the new API key with proper string formatting
            existing_content.append(f'GEMINI_API_KEY="{api_key}"')
            
            # Write back to .env
            with open(env_path, 'w') as f:
                f.write('\n'.join(existing_content) + '\n')
            
            # Reload environment variables
            load_dotenv()
            
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(self, "Success", "API key saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save API key: {str(e)}")
