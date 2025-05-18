import sys
from PyQt5.QtWidgets import QApplication

from backend.vector_store import VectorStore
from frontend.ui import UI

if __name__ == "__main__":
    try:
        # Initialize the vector store
        store = VectorStore()
        print("Syncing ChromaDB with ./docs/ directory")
        store.sync_with_docs_directory()
        print("Sync complete")
        
        # Initialize and run the application
        app = QApplication([])
        app.setStyle('Fusion')  # Use Fusion style for better dark theme support
        window = UI(store)
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error starting DevFlow: {str(e)}")
        sys.exit(1)