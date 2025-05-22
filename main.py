import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import Qt

from backend.vector_store import VectorStore
from frontend.ui import UI
from backend.project_config import ProjectConfig
from frontend.settings_dialog import SettingsDialog
from dotenv import load_dotenv
import os

def check_api_key():
    """Check if Gemini API key exists and prompt user if it doesn't"""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        msg = QMessageBox()
        msg.setWindowTitle("API Key Required")
        msg.setText("Gemini API key is required to proceed.")
        msg.setInformativeText("Would you like to enter your API key now?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setIcon(QMessageBox.Question)
        
        if msg.exec_() == QMessageBox.Yes:
            settings = SettingsDialog()
            if settings.exec_() == SettingsDialog.Rejected:
                return False
            # Reload env after settings dialog
            load_dotenv()
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return False
        else:
            return False
    
    return True

if __name__ == "__main__":
    try:
        # Check for API key before proceeding
        if not check_api_key():
            print("API key is required to run the application.")
            sys.exit(1)
        
        # Initialize the project configuration
        config = ProjectConfig()
        
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