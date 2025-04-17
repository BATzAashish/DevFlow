from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                            QLineEdit, QListWidget, QListWidgetItem, QLabel, 
                            QHBoxLayout, QSplitter, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys

from backend.ai_model import generate_response

class ExpandableMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_menu()
        
    def init_menu(self):
        layout = QVBoxLayout(self)
        self.buttons = []
        self.content_widgets = []
        
        for i in range(8):
            # Create button and content
            button = QPushButton(f"Window {i+1}", self)
            content = QFrame()
            content.setFrameShape(QFrame.StyledPanel)
            content.setStyleSheet("background-color: #2A2F32; margin: 0 10px;")
            content_layout = QVBoxLayout(content)
            content_layout.addWidget(QLabel(f"Content for Window {i+1}"))
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

class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, store, query, parent = None):
        super().__init__(parent)
        self.store = store
        self.query = query
    
    def make_rag_prompt(self, query, relevant_chunks):
        '''
        Construct a prompt for Gemini to generate a structured output
        '''
        escaped_chunks = " ".join(relevant_chunks).replace("'", "").replace('"', '').replace("\n", " ")
        prompt = f"""You are a helpful and informative bot that answers questions using text from the reference chunks below. Provide a clear and concise response, such as a step-by-step guide or explanation, based on the query. If the chunks are irrelevant, provide a general answer based on your knowledge.
        QUESTION: '{query}'
        REFERENCE CHUNKS: '{escaped_chunks}'
        ANSWER:
        """

        return prompt

    def run(self):
        '''
        Does the RAG search processing in background
        '''
        results = self.store.query(self.query)
        if results:
            prompt = self.make_rag_prompt(self.query, results)
            response = generate_response(prompt)
        else:
            response = "No relevant documents found. Please try a different query."
        self.finished.emit(response)

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
        
        # Create container for chat area
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        
        # Set width for chat container (1/3 of screen width)
        screen = QApplication.primaryScreen().size()
        chat_width = int(screen.width() * 0.3)  # 33% of screen width
        chat_container.setMinimumWidth(chat_width)
        chat_container.setMaximumWidth(chat_width)
        
        # chat display area 
        self.chat_list = QListWidget()
        self.chat_list.setStyleSheet("""
            QListWidget {
                background-color: #121B22;
                border: none;
            }
            QListWidget::item {
                border: none;
                margin: 5px;
            }
            QScrollBar:vertical {
                background-color: #121B22;
                width: 12px;
                margin: 16px 0 16px 0;
                border: 1px solid #121B22;
            }
            QScrollBar::handle:vertical {
                background-color: #888888;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #555555;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        self.chat_list.verticalScrollBar().setSingleStep(1)
        chat_layout.addWidget(self.chat_list)

        # input area layout (horizontal for input and button)
        input_layout = QHBoxLayout()
        
        # input field
        self.input_field = QLineEdit()
        self.input_field.setStyleSheet("""
            background-color: #2A2F32;
            color: white;
            border: 1px solid #3A3F41;
            border-radius: 20px;
            padding: 10px 15px;
            font-size: 14px;
        """)
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.returnPressed.connect(self.handle_submit)  # Keep Enter key functionality
        input_layout.addWidget(self.input_field)

        # generate button
        self.submit_button = QPushButton("Generate", self)
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #00A884;  
                color: white;
                border-radius: 10px;  
                border: 1px solid #00A884; 
                padding: 5px 10px;  
            }
            QPushButton:hover {
                background-color: #008C74;  
            }
        """)
        self.submit_button.clicked.connect(self.handle_submit)
        input_layout.addWidget(self.submit_button)

        chat_layout.addLayout(input_layout)
        
        # Add chat container to splitter
        splitter.addWidget(chat_container)
        
        # Add splitter to main layout
        layout.addWidget(splitter)
        self.setLayout(layout)

        # Apply window background
        self.setStyleSheet("background-color: #121B22;")

    def add_message(self, sender, message):
        '''
        Add a message to the chat list with styling.
        '''
        item = QListWidgetItem()
        widget = QLabel(message)
        widget.setWordWrap(True)

        # set background color based on sender
        bg_color = '#6495ED' if sender == 'DevFlow Bot' else '#005C4B' 
        widget.setStyleSheet(f"""
            background-color: {bg_color};
            color: white;
            border-radius: 10px;
            padding: 15px;
            max-width: 700px;
        """)

        widget.adjustSize()
        size = widget.sizeHint()
        size.setHeight(size.height() + 5)  
        item.setSizeHint(size)

        # align messages (right for user, left for bot)
        if sender == 'User':
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            widget.setStyleSheet(widget.styleSheet() + "margin-left: 180px;")
        else:
            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft)
            widget.setStyleSheet(widget.styleSheet() + "margin-right: 180px;")

        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, widget)
        self.chat_list.scrollToBottom()

    def handle_submit(self):
        user_query = self.input_field.text()
        if not user_query:
            return
        
        self.add_message('User', user_query)
        self.input_field.clear()

        # Force UI update to show the message instantly
        QApplication.processEvents()

        # Start RAG processing in thread
        self.worker = Worker(self.store, user_query)
        self.worker.finished.connect(self.on_response_ready)
        self.worker.start()
    
    def on_response_ready(self, response):
        '''
        Handle bot response when worker finishes
        '''
        self.add_message('DevFlow Bot', response)

def run_app(store):
    app = QApplication([])
    window = UI(store)
    window.show()
    sys.exit(app.exec_())