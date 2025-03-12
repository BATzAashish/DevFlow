# DevFlow: AI Programming Assistant

## Overview
DevFlow is an innovative AI-powered programming assistant designed to guide developers through the entire project development lifecycle. Leveraging Retrieval-Augmented Generation (RAG) and the Google Gemini API, DevFlow assists users in planning, coding, testing, deploying, and documenting projects by processing PDF-based documentation and generating tailored responses.

## What We Are Making
We are building DevFlow as a desktop application with a chat-based interface to:
- Support project development through a step-by-step workflow (e.g., technology selection, project setup, implementation, testing, deployment, documentation).
- Provide an interactive RAG chatbot to answer queries, fix errors, and offer project-specific advice based on uploaded PDFs.
- Allow users to start fresh or continue existing projects with saved state management.

## What Has Been Made Till Now
- **PDF Processing**: Extracts and chunks text from PDFs using `pdfplumber` for storage.
- **Vector Storage**: Implements ChromaDB to embed and retrieve PDF chunks, with syncing for the `./docs` directory.
- **RAG System**: Integrates Google Gemini API for query summarization and response generation, with a cross-encoder (`sentence-transformers`) for reranking results.
- **UI**: A PyQt5-based chat interface displaying user queries and bot responses, styled with a dark theme, and supporting Enter key submission.
- **Optimizations**: Added `QThread` for responsive UI during RAG processing and retry logic (up to 3 attempts) for API calls to handle failures.

## What We Are Working On
- **Workflow Steps**: Implementing a left-side panel with expandable tabs for a multi-step process (e.g., choosing technology, setting project location, generating file structure).
- **Code Generation**: Developing `backend/code_generation.py` to automate project setup, environment configuration (e.g., virtual env, Git), and code implementation.
- **Project State Management**: Adding functionality to save and load project settings (e.g., tech stack, file structure) for resuming work.
- **Enhanced Features**: Planning a settings tab and documentation generation (e.g., README creation).

## Requirements
- **Python Version**: 3.12.4
- **Dependencies**: Listed in `requirements.txt`:

```
# PyQt5==5.15.9
# chromadb==0.5.0
# google-generativeai==0.7.2
# pdfplumber==0.11.0
# sentence-transformers==2.7.0
# python-dotenv==1.0.1
# hashlib==20081119
```

## Installation
1. Ensure Python 3.12.4 is installed.
2. Clone the repository:
```
git clone https://github.com/chiraggulati098/DevFlow
cd DevFlow
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Set up your Google Gemini API key in a `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```
5. Place PDF documents in the `./docs` directory (some files are added, but you can add your own also; it will sync them automatically at start up).
6. Run the application:
```
python main.py
```

## Usage
- Open the app and type a development query (e.g., “How do I sort a list in Python?”) in the chat input.
- Press Enter or click “Generate” to see the bot response based on RAG.
- The app syncs with `./docs` on startup to process new or modified PDFs.

## Contributing
Feel free to suggest features or report issues. Contributions are welcome!
