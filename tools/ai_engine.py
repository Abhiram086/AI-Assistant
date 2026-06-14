import json
from openai import OpenAI

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def query_jarvis_core(user_input: str, conversation_history: list) -> dict:
    """Sends input and memory to the local model to extract intelligent routing instructions."""
    
    system_prompt = (
            "You are JARVIS, an autonomous Linux OS agent running on CachyOS with KDE Plasma.\n"
            "Your job is to understand user intent, fix typos, and execute the correct system tool.\n\n"
            
            "AGENT RULES:\n"
            "1. Typo Correction: Silently correct misspelled app names.\n"
            "2. Environment Knowledge: 'settings' or 'control panel' ALWAYS means 'systemsettings'.\n"
            "3. Directory Paths: The user's home directory is /home/abhiram/. ALWAYS use absolute paths for folders.\n"
            "4. Repetition: If the user says 'repeat', execute the last action again.\n"
            "5. Implied Intent: If the user just types an app or folder name, assume they want to open it.\n\n"
            
            "CRITICAL FORMAT RULE:\n"
            "You MUST respond ONLY with a single JSON object containing the key \"tool\".\n"
            "Valid tools are: \"open_app\", \"check_system\", \"chat\".\n\n"
            
            "TOOL DEFINITIONS:\n"
            "- \"open_app\": Launch an app or folder. Always use this for 'settings' (app_name: 'systemsettings').\n"
            "- \"check_system\": ONLY use when the user asks for CPU, RAM, or battery vitals. NEVER use for 'settings' or 'OS info'.\n"
            "- \"chat\": Use to converse, answer questions like 'who am i' or 'what OS is this'.\n\n"
            
            "Examples of PERFECT outputs:\n"
            "{\"tool\": \"chat\", \"response\": \"You are Abhiram, and this is CachyOS.\"}\n"
            "{\"tool\": \"open_app\", \"app_name\": \"dolphin\", \"arguments\": [\"/home/abhiram/Downloads\"]}\n"
            "{\"tool\": \"open_app\", \"app_name\": \"systemsettings\"}\n"
            "{\"tool\": \"check_system\"}\n"
        )

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_input})

    try:
        response = client.chat.completions.create(
            model="local-model",
            messages=messages,
            temperature=0.1,
            timeout=60.0
        )
        
        raw_content = response.choices[0].message.content.strip()
        
        start_idx = raw_content.find('{')
        end_idx = raw_content.rfind('}') + 1
        
        if start_idx != -1 and end_idx != 0:
            clean_json = raw_content[start_idx:end_idx]
        else:
            clean_json = raw_content
            
        try:
            return json.loads(clean_json)
        except json.JSONDecodeError:
            return {"tool": "chat", "response": raw_content}
            
    except Exception as e:
        return {"tool": "chat", "response": f"AI Engine Connection Error: {str(e)}"}