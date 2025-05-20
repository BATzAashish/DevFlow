from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QLabel, QFrame, QHBoxLayout, QMessageBox, QScrollArea)
from PyQt5.QtCore import Qt
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import subprocess
import uuid
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from .tech_stack_dialog import TechStackDialog
from backend.project_config import ProjectConfig
from backend.ai_model import generate_response

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
            "Step 3: Create Project Structure",
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
                                # Ensure imports are working
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                
                # Create a horizontal layout for the venv and git boxes
                hbox = QHBoxLayout()
                hbox.setSpacing(20)

                # Python venv option (only if 'python' in tech stack)
                if 'python' in self.config.tech_stack.lower():
                    venv_frame = QFrame()
                    venv_frame.setStyleSheet("""
                        QFrame {
                            background-color: #23282C;
                            border: 1px solid #3A3F41;
                            border-radius: 4px;
                            margin: 5px;
                        }
                    """)
                    venv_vlayout = QVBoxLayout(venv_frame)
                    venv_vlayout.setContentsMargins(20, 20, 20, 20)
                    venv_vlayout.setSpacing(15)
                    
                    # Create inner frame for content
                    inner_frame = QFrame()
                    inner_frame.setStyleSheet("""
                        QFrame {
                            background-color: #1E2428;
                            border: 1px solid #3A3F41;
                            border-radius: 4px;
                            padding: 15px;
                        }
                    """)
                    inner_layout = QVBoxLayout(inner_frame)
                    inner_layout.setSpacing(15)
                    
                    venv_label = QLabel("Python Virtual Environment Setup")
                    venv_label.setStyleSheet("color: white; font-size: 15px;")
                    venv_label.setAlignment(Qt.AlignCenter)
                    inner_layout.addWidget(venv_label)
                    
                    # Add a stretch to push the button to the bottom
                    inner_layout.addStretch()
                    
                    venv_btn = QPushButton("Create Environment")
                    venv_btn.setFixedHeight(35)
                    venv_btn.setStyleSheet("""
                        QPushButton {
                            background-color: #00A884;
                            color: white;
                            border: none;
                            padding: 8px 0;
                            border-radius: 4px;
                            font-size: 14px;
                            min-width: 200px;
                        }
                        QPushButton:hover {
                            background-color: #008C74;
                        }
                    """)
                    if self.config.has_venv:
                        self.update_button_state(venv_btn, state='exists', is_initial=True)
                    venv_btn.clicked.connect(self.create_python_venv)
                    inner_layout.addWidget(venv_btn, alignment=Qt.AlignCenter)
                    venv_vlayout.addWidget(inner_frame)
                    hbox.addWidget(venv_frame)

                # Git repo option (always shown)
                git_frame = QFrame()
                git_frame.setStyleSheet("""
                    QFrame {
                        background-color: #23282C;
                        border: 1px solid #3A3F41;
                        border-radius: 4px;
                        margin: 5px;
                    }
                """)
                git_vlayout = QVBoxLayout(git_frame)
                git_vlayout.setContentsMargins(20, 20, 20, 20)
                git_vlayout.setSpacing(15)

                # Create inner frame for content
                inner_frame = QFrame()
                inner_frame.setStyleSheet("""
                    QFrame {
                        background-color: #1E2428;
                        border: 1px solid #3F3F41;
                        border-radius: 4px;
                        padding: 15px;
                    }
                """)
                inner_layout = QVBoxLayout(inner_frame)
                inner_layout.setSpacing(15)
                
                git_label = QLabel("Git Repository Setup")
                git_label.setStyleSheet("color: white; font-size: 15px;")
                git_label.setAlignment(Qt.AlignCenter)
                inner_layout.addWidget(git_label)
                
                # Add a stretch to push the button to the bottom
                inner_layout.addStretch()
                
                git_btn = QPushButton("Create Repository")
                git_btn.setFixedHeight(35)
                git_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #00A884;
                        color: white;
                        border: none;
                        padding: 8px 0;
                        border-radius: 4px;
                        font-size: 14px;
                            min-width: 200px;
                        }
                        QPushButton:hover {
                            background-color: #008C74;
                        }                    """)
                if self.config.has_git:
                    self.update_button_state(git_btn, state='exists', is_initial=True)
                git_btn.clicked.connect(self.create_git_repo)
                inner_layout.addWidget(git_btn, alignment=Qt.AlignCenter)
                git_vlayout.addWidget(inner_frame)
                hbox.addWidget(git_frame, 1)  # Add stretch factor 1 to make it expand

                if 'python' in self.config.tech_stack.lower():
                    # Set the first frame to also stretch if it exists
                    hbox.setStretchFactor(venv_frame, 1)
                
                content_layout.addLayout(hbox)
            elif i == 2:  # Step 3: Create Project Structure
                # Create a frame to act as a text box
                structure_frame = QFrame()
                structure_frame.setStyleSheet("""
                    QFrame {
                        background-color: #1E2428;
                        border: 1px solid #3F3F41;
                        border-radius: 4px;
                        margin: 5px;
                    }
                """)
                structure_frame_layout = QVBoxLayout(structure_frame)
                structure_frame_layout.setContentsMargins(15, 15, 15, 15)

                # File structure display area
                structure_text = self.config.file_structure if hasattr(self.config, 'file_structure') and self.config.file_structure.strip() else "No structure generated yet"
                
                # Create scroll area for the structure display
                scroll_area = QScrollArea()
                scroll_area.setWidgetResizable(True)
                scroll_area.setStyleSheet("""
                    QScrollArea {
                        border: none;
                        background-color: #2A2F32;
                        border-radius: 4px;
                    }
                    QScrollBar:vertical {
                        border: none;
                        background: #2A2F32;
                        width: 10px;
                        margin: 0px;
                    }
                    QScrollBar::handle:vertical {
                        background: #3A3F41;
                        min-height: 20px;
                        border-radius: 5px;
                    }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        border: none;
                        background: none;
                    }
                """)

                # Create container widget for the label
                container = QWidget()
                container_layout = QVBoxLayout(container)
                container_layout.setContentsMargins(0, 0, 0, 0)

                self.structure_label = QLabel(structure_text)
                self.structure_label.setStyleSheet("""
                    QLabel {
                        color: white;
                        padding: 15px;
                        background-color: #2A2F32;
                        border-radius: 4px;
                        font-family: "Consolas", "Monaco", "Courier New", monospace;
                        white-space: pre;
                        font-size: 12px;
                        line-height: 1.5;
                        letter-spacing: 0.3px;
                    }
                """)
                self.structure_label.setWordWrap(False)
                self.structure_label.setTextFormat(Qt.PlainText)
                self.structure_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
                
                # Add label to container
                container_layout.addWidget(self.structure_label)
                container_layout.addStretch()
                
                # Set container as scroll area widget
                scroll_area.setWidget(container)
                scroll_area.setMinimumHeight(300)  # Set a good default height
                
                structure_frame_layout.addWidget(scroll_area)

                # Generate button at the bottom
                generate_button = QPushButton("Generate Structure")
                generate_button.setFixedHeight(35)
                generate_button.setStyleSheet("""
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
                generate_button.clicked.connect(self.generate_structure)
                structure_frame_layout.addWidget(generate_button)

                content_layout.addWidget(structure_frame)
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

    def show_error_dialog(self, error_msg, error_id, operation):
        try:
            # Generate AI debug response
            prompt = f"I encountered this error while {operation}:\nError ID: {error_id}\nError: {error_msg}\nPlease explain what might have gone wrong and how to fix it in simple terms."
            debug_response = generate_response(prompt)
            
            # Create detailed error message
            detailed_msg = f"Error ID: {error_id}\n\nError Details:\n{error_msg}\n\nAI Debug Suggestion:\n{debug_response}"
            
            # Show error dialog
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setText("An error occurred")
            msg_box.setDetailedText(detailed_msg)
            msg_box.exec_()
        except Exception as e:
            # Fallback error display if AI fails
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setText(f"Error: {error_msg}\nError ID: {error_id}")
            msg_box.exec_()

    def update_button_state(self, button, state='created', is_initial=False):
        if state == 'created':
            button.setText("✓ Created")
            button.setEnabled(False)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2A2F32;
                    color: #00A884;
                    border: none;
                    padding: 8px 0;
                    border-radius: 4px;
                    font-size: 14px;
                    min-width: 200px;
                }
            """)
        elif is_initial and state == 'exists':
            button.setText("✓ Created")
            button.setEnabled(False)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #2A2F32;
                    color: #00A884;
                    border: none;
                    padding: 8px 0;
                    border-radius: 4px;
                    font-size: 14px;
                    min-width: 200px;
                }
            """)

    def create_python_venv(self):
        project_path = self.config.project_path
        if not project_path:
            QMessageBox.warning(self, "Warning", "Please set up the project path first!")
            return

        venv_path = os.path.join(project_path, 'venv')
        error_id = str(uuid.uuid4())[:8]
        sender_button = self.sender()

        try:
            # Ensure we're in the project directory
            os.makedirs(project_path, exist_ok=True)
            os.chdir(project_path)

            # Create virtual environment
            result = subprocess.run(['python', '-m', 'venv', venv_path],
                                    capture_output=True, text=True, check=True)

            # Update button state and config
            self.update_button_state(sender_button)
            self.config.set_venv_status(True)

            # Show success message
            QMessageBox.information(self, "Success", "Python virtual environment created successfully!")

        except subprocess.CalledProcessError as e:
            self.show_error_dialog(
                f"Failed to create virtual environment:\n{e.stderr}",
                error_id,
                "creating Python virtual environment"
            )
        except Exception as e:
            self.show_error_dialog(
                f"Unexpected error while creating virtual environment:\n{str(e)}",
                error_id,
                "creating Python virtual environment"
            )

    def create_git_repo(self):
        project_path = self.config.project_path
        if not project_path:
            QMessageBox.warning(self, "Warning", "Please set up the project path first!")
            return
            
        error_id = str(uuid.uuid4())[:8]
        sender_button = self.sender()
        
        try:
            # Ensure we're in the project directory
            os.makedirs(project_path, exist_ok=True)
            os.chdir(project_path)
            
            # Initialize git repository
            subprocess.run(['git', 'init'], check=True, capture_output=True, text=True)
            
            # Read and write .gitignore file
            template_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend', 'templates', 'gitignore_template.txt')
            try:
                with open(template_path, 'r') as template_file:
                    gitignore_content = template_file.read()
                with open('.gitignore', 'w') as f:
                    f.write(gitignore_content)
            except Exception as e:
                print(f"Warning: Could not create .gitignore file: {str(e)}")
            
            # Update button state and config
            self.update_button_state(sender_button)
            self.config.set_git_status(True)
            
            # Show success message
            QMessageBox.information(self, "Success", "Git repository initialized successfully!")
            
        except subprocess.CalledProcessError as e:
            self.show_error_dialog(
                f"Failed to initialize git repository:\n{e.stderr}",
                error_id,
                "initializing git repository"
            )
        except Exception as e:
            self.show_error_dialog(
                f"Unexpected error while initializing git repository:\n{str(e)}",
                error_id,
                "initializing git repository"
            )
    
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

    def generate_structure(self):
        if not self.config.tech_stack:
            QMessageBox.warning(self, "Warning", "Please set up the tech stack first!")
            return
            
        if not self.config.project_path:
            QMessageBox.warning(self, "Warning", "Please set up the project path first!")
            return
            
        try:
            # Generate structure using Gemini
            prompt = f"Generate a professional and detailed file structure for a project named \"{self.config.project_name}\". The project description is: \"{self.config.project_description}\". The tech stack to be used is: \"{self.config.tech_stack}\". Provide ONLY the file structure in a clear, hierarchical format. Do not include any explanations, descriptions, or code snippets."
            response = generate_response(prompt)
                        
            # Update the UI and save to config
            self.structure_label.setText(response)
            if hasattr(self.config, 'update_file_structure'):
                self.config.update_file_structure(response)
                
        except Exception as e:
            error_id = str(uuid.uuid4())[:8]
            self.show_error_dialog(
                str(e),
                error_id,
                "generating project structure"
            )
