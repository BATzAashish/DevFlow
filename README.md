# DevFlow: AI Developer Assistant

## Overview
DevFlow is a comprehensive AI-powered desktop application designed to revolutionize the software development workflow. By combining Retrieval-Augmented Generation (RAG) with the Google Gemini API, DevFlow provides an intelligent assistant that guides developers through every phase of project development, from initial planning to deployment and documentation.

## Core Features

### 1. Intelligent Project Management
- **Project Setup Wizard**: Intuitive interface for creating new projects with customizable settings
- **Tech Stack Selection**: Flexible technology stack configuration through a dedicated dialog
- **Environment Management**: Automated setup of Python virtual environments and Git repositories
- **Project State Management**: Persistent storage of project configurations and progress

### 2. RAG-Powered Knowledge System
- **PDF Processing**: Advanced text extraction from PDFs using `pdfplumber` with intelligent chunking
- **Vector Storage**: Efficient document storage and retrieval using ChromaDB
- **Smart Search**: 
  - Automated syncing with `./docs` directory
  - Query summarization using Gemini API
  - Response reranking using cross-encoder models
  - Retry logic for API resilience

### 3. Development Workflow Support
- **Step-by-Step Guidance**: Structured development process through expandable tabs:
  1. Tech Stack Selection
  2. Environment Setup
  3. Project Structure Generation
  4. Implementation Assistance
  5. Testing Strategy
  6. Deployment Planning
  7. Documentation Generation

### 4. Modern User Interface
- **Split View Design**: 
  - Left panel: Development workflow steps
  - Right panel: Interactive chat interface
- **Dark Theme**: Professional dark mode with accent colors
- **Real-time Updates**: Responsive UI with background processing
- **Code Display**: Syntax-highlighted code snippets and command widgets

### 5. Chat Assistant
- **Context-Aware Responses**: Intelligent responses based on project context and documentation
- **History Management**: Conversation history tracking with configurable length
- **Async Processing**: Non-blocking UI during response generation
- **Error Handling**: Comprehensive error management with AI-powered debugging suggestions

## Technical Stack
- **Frontend**: PyQt5 with custom styling and components
- **Backend**:
  - Google Gemini API for AI capabilities
  - ChromaDB for vector storage
  - Sentence Transformers for response ranking
- **Document Processing**: pdfplumber for text extraction
- **Environment**: Python 3.12.4

## Project Structure
```
DevFlow/
├── backend/              # Core backend functionality
│   ├── ai_model.py      # Gemini API integration
│   ├── pdf_processor.py # PDF handling
│   ├── vector_store.py  # ChromaDB operations
│   └── project_config.py # Project state management
├── frontend/            # UI components
│   ├── ui.py           # Main window
│   ├── chat_interface.py # Chat implementation
│   ├── menu_interface.py # Workflow steps
│   └── components.py    # Reusable UI elements
├── docs/               # Documentation storage
└── chroma_db/         # Vector database storage
```

## Installation

### Prerequisites
- Python 3.12.4

### Setup
1. Clone the repository:
```bash
git clone https://github.com/chiraggulati098/DevFlow
cd DevFlow
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Gemini API key in `.env`:
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python main.py
```

## Usage
1. Launch DevFlow and enter project details in the setup wizard
2. Follow the step-by-step workflow in the left panel:
   - Configure your tech stack
   - Set up development environment
   - Generate and customize project structure
   - Implement features with AI assistance
   - Define testing and deployment strategies
   - Generate comprehensive documentation
3. Use the chat interface for real-time assistance and queries


## Requirements
- **Python Version**: 3.12.4
- **Dependencies**: Listed in `requirements.txt`