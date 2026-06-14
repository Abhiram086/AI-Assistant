import subprocess

# The Translation Layer: Map common names or AI guesses to your true CachyOS binaries
APP_ALIASES = {
    "files": "dolphin",
    "nautilus": "dolphin",
    "file_manager": "dolphin",
    "zenbrowser": "zen-browser",  # Adjusted guess for Zen
    "zen": "zen-browser",         # Adjusted guess for Zen
    "browser": "firefox",
    "code": "code",               
    "terminal": "konsole",          
    "settings": "systemsettings", # KDE Plasma Settings mapped correctly
    "system settings": "systemsettings",
    "control panel": "systemsettings"
}

def launch_application(app_name: str, arguments: list = None) -> str:
    """Attempts to run a system binary using subprocess, with alias resolution and flags."""
    try:
        true_binary = APP_ALIASES.get(app_name.lower(), app_name.lower())
        
        command = [true_binary]
        if arguments and isinstance(arguments, list):
            command.extend(arguments)
            
        subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if arguments:
            return f"Successfully opened {true_binary} with options: {arguments}"
        return f"Successfully opened {true_binary}."
        
    except FileNotFoundError:
        return f"Application '{true_binary}' (resolved from '{app_name}') not found in system PATH."
    except Exception as e:
        return f"Failed to execute {app_name}: {str(e)}"