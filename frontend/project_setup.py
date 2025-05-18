from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QLineEdit, QFileDialog, QWidget,
                            QDesktopWidget)
from PyQt5.QtCore import Qt

class ProjectSetupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Welcome to DevFlow")
        self.setStyleSheet("""
            QDialog {
                background-color: #121B22;
            }
            QLabel {
                color: white;
                font-size: 14px;
            }
            QLabel#welcomeLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
                margin: 20px 0;
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
            QPushButton:disabled {
                background-color: #2A2F32;
                color: #666666;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #3A3F41;
                border-radius: 4px;
                background-color: #2A2F32;
                color: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 1px solid #00A884;
            }
            QLineEdit:disabled {
                background-color: #1E2428;
                color: #666666;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 20, 30, 30)
        main_layout.setSpacing(15)
        
        # Center the dialog on screen
        self.center_on_screen()
        
        # Welcome message
        welcome_label = QLabel("Welcome to DevFlow!")
        welcome_label.setObjectName("welcomeLabel")
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)
        
        # Form layout for inputs
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(10)
        
        # Project name section
        name_label = QLabel("Project Name:")
        self.project_name = QLineEdit()
        self.project_name.setPlaceholderText("Enter project name (e.g., MyCalculator)")
        form_layout.addWidget(name_label)
        form_layout.addWidget(self.project_name)
        
        # Project description section
        description_label = QLabel("What would you like to build?")
        self.project_description = QLineEdit()
        self.project_description.setPlaceholderText("Describe your project (e.g., A simple calculator application)")
        form_layout.addWidget(description_label)
        form_layout.addWidget(self.project_description)
        
        # Location section
        location_label = QLabel("Where would you like to create your project?")
        form_layout.addWidget(location_label)
        
        # Location input and browse button in horizontal layout
        location_widget = QWidget()
        location_layout = QHBoxLayout(location_widget)
        location_layout.setContentsMargins(0, 0, 0, 0)
        location_layout.setSpacing(10)
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Select project location...")
        self.location_input.setReadOnly(True)
        
        browse_button = QPushButton("Browse...")
        browse_button.setFixedWidth(100)
        browse_button.clicked.connect(self.browse_location)
        
        location_layout.addWidget(self.location_input)
        location_layout.addWidget(browse_button)
        form_layout.addWidget(location_widget)
        
        main_layout.addWidget(form_widget)
        
        # Add some spacing before the create button
        main_layout.addSpacing(10)
        
        # Create project button
        self.create_button = QPushButton("Create Project")
        self.create_button.clicked.connect(self.accept)
        self.create_button.setEnabled(False)
        self.create_button.setFixedHeight(40)
        main_layout.addWidget(self.create_button)
        
        # Update button state when input changes
        self.project_description.textChanged.connect(self.update_create_button)
        self.location_input.textChanged.connect(self.update_create_button)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        
    def browse_location(self):
        location = QFileDialog.getExistingDirectory(
            self,
            "Select Project Location",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if location:
            self.location_input.setText(location)
            
    def update_create_button(self):
        # Enable create button only when all fields are filled
        self.create_button.setEnabled(
            bool(self.project_name.text().strip()) and
            bool(self.project_description.text().strip()) and 
            bool(self.location_input.text().strip())
        )
    
    def center_on_screen(self):
        # Get the screen geometry
        screen = QDesktopWidget().screenGeometry()
        # Get the dialog geometry
        dialog = self.geometry()
        # Center the dialog
        x = (screen.width() - dialog.width()) // 2
        y = (screen.height() - dialog.height()) // 2
        self.move(x, y)
    
    def get_project_info(self):
        return {
            'name': self.project_name.text().strip(),
            'description': self.project_description.text().strip(),
            'location': self.location_input.text().strip()
        }
