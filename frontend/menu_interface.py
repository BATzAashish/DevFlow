from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QFrame, QHBoxLayout)
from PyQt5.QtCore import Qt
from .tech_stack_dialog import TechStackDialog
from backend.project_config import ProjectConfig

class ExpandableMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = ProjectConfig()
        self.layout = QVBoxLayout(self)
        self.init_menu()
        
    def init_menu(self):
        layout = self.layout
        # Remove all widgets from layout (but not the layout itself)
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        self.buttons = []
        self.content_widgets = []
        
        step_names = [
            "Step 1: Choose Tech Stack",
            "Step 2: Environment and Repository Setup",
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
                tech_stack_text = self.config.tech_stack if self.config.tech_stack.strip() else "No tech stack selected"
                self.tech_stack_label = QLabel(tech_stack_text)
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
            elif i == 1:  # Step 2: Environment and Repository Setup
                # Python venv option (only if 'python' in tech stack)
                if 'python' in self.config.tech_stack.lower():
                    venv_frame = QFrame()
                    venv_frame.setStyleSheet("""
                        QFrame {
                            background-color: #23282C;
                            border: 1px solid #3A3F41;
                            border-radius: 4px;
                            margin: 5px 0 10px 0;
                        }
                    """)
                    venv_layout = QHBoxLayout(venv_frame)
                    venv_label = QLabel("Python Virtual Environment Setup")
                    venv_label.setStyleSheet("color: white; font-size: 15px;")
                    venv_layout.addWidget(venv_label)
                    venv_layout.addStretch()
                    venv_btn = QPushButton("Create")
                    venv_btn.setFixedHeight(30)
                    venv_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #00A884;
                            color: white;
                            border: none;
                            padding: 6px 16px;
                            border-radius: 4px;
                            font-size: 13px;
                        }
                        QPushButton:hover {
                            background-color: #008C74;
                        }
                    """)
                    venv_btn.clicked.connect(self.create_python_venv)
                    venv_layout.addWidget(venv_btn)
                    content_layout.addWidget(venv_frame)

                # Git repo option (always shown)
                git_frame = QFrame()
                git_frame.setStyleSheet("""
                    QFrame {
                        background-color: #23282C;
                        border: 1px solid #3A3F41;
                        border-radius: 4px;
                        margin: 5px 0 10px 0;
                    }
                """)
                git_layout = QHBoxLayout(git_frame)
                git_label = QLabel("Git Repository Setup")
                git_label.setStyleSheet("color: white; font-size: 15px;")
                git_layout.addWidget(git_label)
                git_layout.addStretch()
                git_btn = QPushButton("Create")
                git_btn.setFixedHeight(30)
                git_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #00A884;
                        color: white;
                        border: none;
                        padding: 6px 16px;
                        border-radius: 4px;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #008C74;
                    }
                """)
                git_btn.clicked.connect(self.create_git_repo)
                git_layout.addWidget(git_btn)
                content_layout.addWidget(git_frame)
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

    def create_python_venv(self):
        # TODO: Implement python venv creation logic
        print("Python virtual environment creation requested.")

    def create_git_repo(self):
        # TODO: Implement git repository creation logic
        print("Git repository creation requested.")
    
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
        dialog = TechStackDialog(self.config.tech_stack, self)
        if dialog.exec_() == TechStackDialog.Accepted:
            tech_stack = dialog.get_tech_stack()
            self.config.update_tech_stack(tech_stack)
            # Find which step is currently expanded
            expanded_index = None
            for idx, content in enumerate(self.content_widgets):
                if content.isVisible():
                    expanded_index = idx
                    break
            # Refresh the menu and restore expanded state
            self.refresh_menu(expanded_index)

    def refresh_menu(self, expand_index=None):
        # Just re-initialize menu (widgets are cleared in init_menu)
        self.init_menu()
        # Restore expanded state if needed
        if expand_index is not None and 0 <= expand_index < len(self.content_widgets):
            self.content_widgets[expand_index].setVisible(True)
            # Also update button style
            self.buttons[expand_index].setStyleSheet(self.buttons[expand_index].styleSheet().replace("background-color: #2A2F32", "background-color: #3A3F41"))
