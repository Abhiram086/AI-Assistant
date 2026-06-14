import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QTextEdit
from tools.apps import launch_application

class JarvisUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("JARVIS OS")
        self.resize(500, 400)
        
        # Layout setup
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Output Display
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4; font-size: 14px; padding: 10px;")
        self.output_area.setPlaceholderText("JARVIS Terminal Output...")
        layout.addWidget(self.output_area)
        
        # Input Box
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 14px; padding: 5px;")
        self.input_line.setPlaceholderText("Type a command (e.g., 'open firefox')...")
        self.input_line.returnPressed.connect(self.handle_command)
        layout.addWidget(self.input_line)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def handle_command(self):
        query = self.input_line.text().strip()
        if not query:
            return
        
        # Show user input
        self.output_area.append(f"\n> {query}")
        self.input_line.clear()
        
        # Hardcoded Phase 1 logic
        normalized_query = query.lower()
        if normalized_query.startswith("open "):
            target_app = normalized_query.replace("open ", "").strip()
            self.output_area.append("JARVIS: Executing system call...")
            result = launch_application(target_app)
            self.output_area.append(f"JARVIS: {result}")
        else:
            self.output_area.append("JARVIS: Unrecognized command. Try 'open firefox' or 'open kitty'.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisUI()
    window.show()
    sys.exit(app.exec())