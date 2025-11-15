"""
History Management System
Save and load calculation history to/from JSON
"""

import json
import os
from datetime import datetime
from pathlib import Path

# Define history file path
HISTORY_DIR = Path("data")
HISTORY_FILE = HISTORY_DIR / "history.json"


def initialize_history_file():
    """
    Initialize the history file and directory if they don't exist
    """
    # Create data directory if it doesn't exist
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create empty history file if it doesn't exist
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f, indent=2)


def load_history():
    """
    Load calculation history from JSON file
    
    Returns:
        list: List of history entries
    """
    initialize_history_file()
    
    try:
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
            return history
    except json.JSONDecodeError:
        # If file is corrupted, return empty list
        return []
    except Exception as e:
        print(f"Error loading history: {e}")
        return []


def save_to_history(module_name, inputs, outputs):
    """
    Save a calculation to history
    
    Args:
        module_name: Name of the physics module
        inputs: Dictionary of input parameters
        outputs: Dictionary of calculated outputs
    """
    initialize_history_file()
    
    try:
        # Load existing history
        history = load_history()
        
        # Create new entry
        entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "module": module_name,
            "inputs": inputs,
            "outputs": outputs
        }
        
        # Append and save
        history.append(entry)
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
            
        print(f"Saved to history: {module_name}")
        
    except Exception as e:
        print(f"Error saving to history: {e}")


def clear_history():
    """
    Clear all history entries
    """
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f, indent=2)
        print("History cleared")
    except Exception as e:
        print(f"Error clearing history: {e}")


def get_history_by_module(module_name):
    """
    Get all history entries for a specific module
    
    Args:
        module_name: Name of the physics module
        
    Returns:
        list: Filtered list of history entries
    """
    history = load_history()
    return [entry for entry in history if entry.get("module") == module_name]


def get_recent_history(count=10):
    """
    Get the most recent history entries
    
    Args:
        count: Number of recent entries to retrieve
        
    Returns:
        list: List of recent history entries
    """
    history = load_history()
    return history[-count:] if len(history) > count else history


def export_history_to_text(filename="history_export.txt"):
    """
    Export history to a human-readable text file
    
    Args:
        filename: Name of the output file
    """
    history = load_history()
    
    try:
        with open(filename, 'w') as f:
            f.write("Physics Calculator - Calculation History\n")
            f.write("=" * 50 + "\n\n")
            
            for i, entry in enumerate(history, 1):
                f.write(f"Entry #{i}\n")
                f.write(f"Date: {entry['timestamp']}\n")
                f.write(f"Module: {entry['module']}\n")
                f.write(f"Inputs: {entry['inputs']}\n")
                f.write(f"Outputs: {entry['outputs']}\n")
                f.write("-" * 50 + "\n\n")
        
        print(f"History exported to {filename}")
    except Exception as e:
        print(f"Error exporting history: {e}")


def get_recent_calculations(count=5):
    """
    Get the most recent calculations
    
    Args:
        count: Number of recent calculations to retrieve
        
    Returns:
        list: List of recent calculation entries
    """
    history = load_history()
    return history[-count:] if len(history) > count else history


def get_total_calculations():
    """
    Get total number of calculations saved
    
    Returns:
        int: Total number of calculations
    """
    history = load_history()
    return len(history)


def clear_all_history():
    """
    Clear all calculation history
    
    Returns:
        bool: True if successful
    """
    try:
        with open(HISTORY_FILE, 'w') as f:
            json.dump([], f, indent=2)
        print("All history cleared")
        return True
    except Exception as e:
        print(f"Error clearing history: {e}")
        return False


def get_recent_calculations(count=5):
    """Get the most recent calculations"""
    history = load_history()
    return history[-count:] if history else []


def get_total_calculations():
    """Get total number of calculations saved"""
    history = load_history()
    return len(history)


def clear_all_history():
    """Clear all calculation history"""
    history_file = Path(__file__).parent.parent / "data" / "history.json"
    history_file.write_text("[]")
    return True
