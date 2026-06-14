import subprocess

def launch_application(app_name: str) -> str:
    """Attempts to run a system binary using subprocess."""
    try:
        # Popen runs the process in the background so it doesn't freeze the GUI
        subprocess.Popen([app_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Successfully opened {app_name}."
    except FileNotFoundError:
        return f"Application '{app_name}' not found in system."
    except Exception as e:
        return f"Failed to open {app_name}: {str(e)}"