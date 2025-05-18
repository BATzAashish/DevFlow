from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt
from .tech_stack_dialog import TechStackDialog

class ExpandableMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tech_stack = ""
        self.init_menu()
        
    def init_menu(self):
        layout = QVBoxLayout(self)
        self.buttons = []
        self.content_widgets = []
        
        step_names = [
            "Step 1: Choose Tech Stack",
            "Window 2",
            "Window 3",
            "Window 4",
            "Window 5",
            "Window 6",
            "Window 7",
            "Window 8"
        ]
        
        for i in range(8):
            # Create button and content
            button = QPushButton(step_names[i], self)
            content = QFrame()
            content.setFrameShape(QFrame.StyledPanel)
            content.setStyleSheet("background-color: #2A2F32; margin: 0 10px;")
            content_layout = QVBoxLayout(content)
            
            if i == 0:  # Special handling for Step 1
                # Create a frame to act as a text box
                tech_frame = QFrame()
                tech_frame.setStyleSheet("""
                    QFrame {
                        background-color: #1E2428;
                        border: 1px solid #3A3F41;
                        border-radius: 4px;
                        margin: 5px;
                    }
                """)
                tech_frame_layout = QVBoxLayout(tech_frame)
                tech_frame_layout.setContentsMargins(15, 15, 15, 15)
                
                # Tech stack display area
                self.tech_stack_label = QLabel("No tech stack selected")
                self.tech_stack_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        padding: 10px;
                        min-height: 100px;
                        background-color: #2A2F32;
                        border-radius: 4px;
                    }
                """)
                self.tech_stack_label.setWordWrap(True)
                self.tech_stack_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                tech_frame_layout.addWidget(self.tech_stack_label)
                
                # Edit button at the bottom
                edit_button = QPushButton("Edit")
                edit_button.setFixedHeight(35)
                edit_button.setStyleSheet("""
                    QPushButton {
                        background-color: #00A884;
                        color: white;
                        border: none;
                        padding: 8px;
                        border-radius: 4px;
                        font-size: 14px;
                    }
                    QPushButton:hover {
                        background-color: #008C74;
                    }
                """)
                edit_button.clicked.connect(self.edit_tech_stack)
                tech_frame_layout.addWidget(edit_button)
                
                content_layout.addWidget(tech_frame)
            else:
                content_layout.addWidget(QLabel(f"Content for {step_names[i]}"))
            content.setVisible(False)
            
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2A2F32;
                    color: white;
                    border: none;
                    text-align: left;
                    padding: 10px;
                    margin: 2px 10px;
                }
                QPushButton:hover {
                    background-color: #3A3F41;
                }
            """)
            
            layout.addWidget(button)
            layout.addWidget(content)
            
            self.buttons.append(button)
            self.content_widgets.append(content)
            
            button.clicked.connect(lambda checked, index=i: self.toggle_content(index))
    
    def toggle_content(self, index):
        # Hide all other content widgets
        for i, content in enumerate(self.content_widgets):
            if i != index:
                content.setVisible(False)
                self.buttons[i].setStyleSheet(self.buttons[i].styleSheet().replace("background-color: #3A3F41", "background-color: #2A2F32"))
        
        # Toggle the clicked content
        current_content = self.content_widgets[index]
        is_visible = current_content.isVisible()
        current_content.setVisible(not is_visible)
        
        # Update button style
        if not is_visible:
            self.buttons[index].setStyleSheet(self.buttons[index].styleSheet().replace("background-color: #2A2F32", "background-color: #3A3F41"))
        else:
            self.buttons[index].setStyleSheet(self.buttons[index].styleSheet().replace("background-color: #3A3F41", "background-color: #2A2F32"))
    
    def edit_tech_stack(self):
        dialog = TechStackDialog(self.tech_stack, self)
        if dialog.exec_() == TechStackDialog.Accepted:
            self.tech_stack = dialog.get_tech_stack()
            self.tech_stack_label.setText(self.tech_stack if self.tech_stack else "No tech stack selected")
