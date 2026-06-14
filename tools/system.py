import psutil

def get_system_stats() -> str:
    """Retrieves CPU, RAM, and Battery information."""
    try:
        # Get CPU usage (1 second interval for accuracy)
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # Get RAM usage
        ram = psutil.virtual_memory()
        ram_total = round(ram.total / (1024**3), 1)  # Convert bytes to GB
        ram_used = round(ram.used / (1024**3), 1)
        ram_percent = ram.percent
        
        # Get Battery (if applicable)
        battery = psutil.sensors_battery()
        if battery:
            batt_percent = battery.percent
            batt_plugged = " (Plugged In)" if battery.power_plugged else " (On Battery)"
            batt_str = f"{batt_percent}%{batt_plugged}"
        else:
            batt_str = "No battery detected"

        # Format the output report
        report = (
            f"System Vitals:\n"
            f"• CPU Usage: {cpu_usage}%\n"
            f"• RAM Usage: {ram_used}GB / {ram_total}GB ({ram_percent}%)\n"
            f"• Battery: {batt_str}"
        )
        return report
        
    except Exception as e:
        return f"Failed to retrieve system stats: {str(e)}"