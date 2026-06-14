import sys
import json  # <-- Add this import
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit, QTextEdit
from tools.apps import launch_application
from tools.system import get_system_stats
from tools.ai_engine import query_jarvis_core

class JarvisUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.memory = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("JARVIS OS")
        self.resize(500, 400)
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4; font-size: 14px; padding: 10px;")
        self.output_area.setPlaceholderText("JARVIS Terminal Output...")
        layout.addWidget(self.output_area)
        
        self.input_line = QLineEdit()
        self.input_line.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 14px; padding: 5px;")
        self.input_line.setPlaceholderText("Ask JARVIS anything or issue a command...")
        self.input_line.returnPressed.connect(self.handle_command)
        layout.addWidget(self.input_line)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def handle_command(self):
        query = self.input_line.text().strip()
        if not query:
            return
        
        self.output_area.append(f"\n> {query}")
        self.input_line.clear()
        self.output_area.append("JARVIS: Processing token sequence...")
        QApplication.processEvents()
        
        # 1. Ask the AI
        ai_blueprint = query_jarvis_core(query, self.memory)
        
        # --- DEFENSIVE AUTOCORRECTION LAYER ---
        # If the AI hallucinates and forgets the "tool" key, we fix it automatically
        if "tool" not in ai_blueprint:
            if "chat" in ai_blueprint:
                ai_blueprint = {"tool": "chat", "response": ai_blueprint["chat"]}
            elif "response" in ai_blueprint:
                ai_blueprint = {"tool": "chat", "response": ai_blueprint["response"]}
        # --------------------------------------
        
        tool_choice = ai_blueprint.get("tool")
        
        # 2. Save memory ensuring we store the RAW JSON string, keeping the pattern strict
        self.memory.append({"role": "user", "content": query})
        self.memory.append({"role": "assistant", "content": json.dumps(ai_blueprint)})
        
        # 3. Execute
        if tool_choice == "open_app":
            target_binary = ai_blueprint.get("app_name", "")
            app_args = ai_blueprint.get("arguments", None)
            
            self.output_area.append(f"JARVIS: [Intent Mode] Target: '{target_binary}'")
            result = launch_application(target_binary, app_args)
            self.output_area.append(f"JARVIS: {result}")
            
        elif tool_choice == "check_system":
            self.output_area.append("JARVIS: [Intent Mode] Fetching kernel diagnostics...")
            result = get_system_stats()
            self.output_area.append(f"JARVIS:\n{result}")
            
        elif tool_choice == "chat":
            conversational_reply = ai_blueprint.get("response", "Internal routing anomaly encountered.")
            self.output_area.append(f"JARVIS: {conversational_reply}")
            
        else:
            self.output_area.append(f"JARVIS: Routing matrix error. Raw AI output: {ai_blueprint}")
            
        if len(self.memory) > 10:
            self.memory = self.memory[-10:]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = JarvisUI()
    window.show()
    sys.exit(app.exec())