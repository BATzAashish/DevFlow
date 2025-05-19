from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                            QLineEdit, QListWidget, QListWidgetItem, QLabel, 
                            QHBoxLayout)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication
from backend.project_config import ProjectConfig

from backend.ai_model import generate_response

class Worker(QThread):
    finished = pyqtSignal(str)

    def __init__(self, store, query, parent = None):
        super().__init__(parent)
        self.store = store
        self.query = query
        self.project_config = ProjectConfig()
    
    def make_rag_prompt(self, query, relevant_chunks):
        escaped_chunks = " ".join(relevant_chunks).replace("'", "").replace('"', '').replace("\n", " ")
        project_info = self.project_config.get_project_info()
        prompt = f"""You are a helpful and informative bot that answers questions using text from the reference chunks below. You have access to the current project context which you should use to provide more relevant answers.
        
        PROJECT CONTEXT:
        {project_info}
        
        QUESTION: '{query}'
        REFERENCE CHUNKS: '{escaped_chunks}'
        
        Provide a clear and concise response, such as a step-by-step guide or explanation, based on the query and project context. If the chunks are irrelevant, provide a general answer based on your knowledge while still considering the project context.
        
        ANSWER:
        """
        print(prompt)
        return prompt

    def run(self):
        results = self.store.query(self.query)
        if results:
            prompt = self.make_rag_prompt(self.query, results)
            response = generate_response(prompt)
        else:
            response = "No relevant documents found. Please try a different query."
        self.finished.emit(response)

class ChatInterface(QWidget):
    def __init__(self, store, parent=None):
        super().__init__(parent)
        self.store = store
        self.init_chat_interface()
    
    def init_chat_interface(self):
        chat_layout = QVBoxLayout(self)
        
        # chat display area 
        self.chat_list = QListWidget()
        self.chat_list.setStyleSheet("""
            QListWidget {
                background-color: #121B22;
                border: none;
            }
            QListWidget::item {
                border: none;
                padding: 0px;
                margin: 0px;
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
            QScrollBar:horizontal {
                height: 0px;
                background: transparent;
            }
        """)
        self.chat_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.chat_list.verticalScrollBar().setSingleStep(1)
        chat_layout.addWidget(self.chat_list)

        # input area layout
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
        self.input_field.returnPressed.connect(self.handle_submit)
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

    def add_message(self, sender, message):
        item = QListWidgetItem()
        widget = QLabel(message)
        
        metrics = widget.fontMetrics()
        text_width = metrics.horizontalAdvance(message)

        container = QWidget()
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(15, 2, 15, 2)
        container_layout.setSpacing(0)

        screen = QApplication.primaryScreen().size()
        chat_width = int(screen.width() * 0.3)
        message_max_width = int(chat_width * 0.75)

        widget.setWordWrap(text_width > message_max_width)

        if sender == 'User':
            bg_color = '#005C4B'
            container_layout.addStretch()
            margin_style = "margin: 3px 0px 3px 0px;"
        else:
            bg_color = '#6495ED'
            margin_style = "margin: 3px 0px 3px 0px;"

        widget.setStyleSheet(f"""
            background-color: {bg_color};
            color: white;
            border-radius: 10px;
            padding: 10px 14px;
            {margin_style}
        """)
        
        widget.setMaximumWidth(message_max_width)

        if sender == 'User':
            container_layout.addStretch()
        container_layout.addWidget(widget)

        widget.adjustSize()
        
        size = widget.sizeHint()
        container.setFixedHeight(size.height() + 6)
        
        item.setSizeHint(container.sizeHint())

        self.chat_list.addItem(item)
        self.chat_list.setItemWidget(item, container)
        self.chat_list.scrollToBottom()

    def handle_submit(self):
        user_query = self.input_field.text()
        if not user_query:
            return
        
        self.add_message('User', user_query)
        self.input_field.clear()

        QApplication.processEvents()

        self.worker = Worker(self.store, user_query)
        self.worker.finished.connect(self.on_response_ready)
        self.worker.start()
    
    def on_response_ready(self, response):
        self.add_message('DevFlow Bot', response)
