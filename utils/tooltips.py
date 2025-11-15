"""
Tooltips and Hover Help
Display helpful hints when hovering over widgets
"""

import customtkinter as ctk
from tkinter import Toplevel


class ToolTip:
    """Create a tooltip for a Tkinter widget"""
    
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        
        widget.bind("<Enter>", self.on_enter)
        widget.bind("<Leave>", self.on_leave)
    
    def on_enter(self, event=None):
        """Show tooltip on mouse enter"""
        if self.tooltip:
            return
        
        # Get coordinates
        x = self.widget.winfo_rootx() + self.widget.winfo_width() // 2
        y = self.widget.winfo_rooty() - 30
        
        # Create tooltip window
        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = ctk.CTkLabel(
            self.tooltip,
            text=self.text,
            font=ctk.CTkFont(size=9),
            fg_color="#404040",
            text_color="#FFFFFF"
        )
        label.pack(ipadx=5, ipady=3)
    
    def on_leave(self, event=None):
        """Hide tooltip on mouse leave"""
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None


# Tooltip texts for each module
KINEMATICS_TOOLTIPS = {
    "u": "Initial velocity - speed at the start of motion (m/s)",
    "v": "Final velocity - speed at the end of motion (m/s)",
    "a": "Acceleration - rate of change of velocity (m/s²)\nPositive = speeding up, Negative = slowing down",
    "t": "Time - duration of motion (seconds)",
    "s": "Displacement - total distance traveled (meters)"
}

OHMS_LAW_TOOLTIPS = {
    "V": "Voltage - electrical potential difference (Volts)\nBatteries: 1.5V (AA), 12V (car), 120V (US outlet)",
    "I": "Current - flow of electric charge (Amperes)\nLED draws ~20mA, Motor draws ~5A",
    "R": "Resistance - opposition to current flow (Ohms)\nCopper wire: ~0.01Ω, Light bulb: ~100Ω"
}

ENERGY_TOOLTIPS = {
    "m": "Mass - amount of matter (kilograms)\nTypical: Person ~70kg, Car ~1500kg",
    "v": "Velocity - speed of motion (m/s)\nRunning: 5m/s, Car: 25m/s (56 mph)",
    "h": "Height - vertical distance above ground (meters)",
    "g": "Gravity - acceleration due to gravity (~9.8 m/s² on Earth)"
}

MOMENTUM_TOOLTIPS = {
    "m1": "Mass of first object (kilograms)",
    "v1": "Velocity of first object (m/s)\nCan be negative for opposite direction",
    "m2": "Mass of second object (kilograms)",
    "v2": "Velocity of second object (m/s)\nCan be negative for opposite direction"
}

OPTICS_TOOLTIPS = {
    "f": "Focal length - distance where light focuses (cm)\nSmaller f = stronger magnification",
    "u": "Object distance - distance from object to lens (cm)",
    "v": "Image distance - distance from image to lens (cm)\nNegative = virtual image"
}


def create_tooltip(widget, text):
    """Helper function to create a tooltip"""
    return ToolTip(widget, text)
