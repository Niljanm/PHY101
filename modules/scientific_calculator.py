"""
Scientific Calculator Module
Advanced mathematical operations and calculations
"""

import customtkinter as ctk
import math
from tkinter import messagebox
from utils.validators import safe_float

class ScientificCalculatorModule:
    def __init__(self, parent, save_callback):
        self.parent = parent
        self.save_callback = save_callback
        self.expression = ""
        
        # Configure parent grid
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            parent,
            text="Scientific Calculator",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=4, pady=(10, 15), sticky="w", padx=15)
        
        # Create calculator frame
        self.create_calculator(parent)
        
    def create_calculator(self, parent):
        """Create the calculator UI"""
        calc_frame = ctk.CTkFrame(parent)
        calc_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=15, pady=(0, 15))
        calc_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Display label
        self.display_label = ctk.CTkLabel(
            calc_frame,
            text="0",
            font=ctk.CTkFont(size=24, family="Courier", weight="bold")
        )
        self.display_label.grid(row=0, column=0, columnspan=4, sticky="ew", pady=10, padx=5)
        
        # Button layout
        buttons = [
            # Row 1
            [("C", self.clear, "#c74a4a"), ("←", self.backspace, "#c74a4a"), ("(", lambda: self.append_to_expr("("), "#3a7a7a"), (")", lambda: self.append_to_expr(")"), "#3a7a7a")],
            # Row 2
            [("7", lambda: self.append_to_expr("7"), "#404040"), ("8", lambda: self.append_to_expr("8"), "#404040"), ("9", lambda: self.append_to_expr("9"), "#404040"), ("/", lambda: self.append_to_expr("/"), "#b39f3a")],
            # Row 3
            [("4", lambda: self.append_to_expr("4"), "#404040"), ("5", lambda: self.append_to_expr("5"), "#404040"), ("6", lambda: self.append_to_expr("6"), "#404040"), ("×", lambda: self.append_to_expr("*"), "#b39f3a")],
            # Row 4
            [("1", lambda: self.append_to_expr("1"), "#404040"), ("2", lambda: self.append_to_expr("2"), "#404040"), ("3", lambda: self.append_to_expr("3"), "#404040"), ("-", lambda: self.append_to_expr("-"), "#b39f3a")],
            # Row 5
            [("0", lambda: self.append_to_expr("0"), "#404040"), (".", lambda: self.append_to_expr("."), "#404040"), ("=", self.calculate_expr, "#4a8c4a"), ("+", lambda: self.append_to_expr("+"), "#b39f3a")],
            # Row 6 - Scientific functions
            [("sin", lambda: self.sci_func("sin"), "#6b5a8a"), ("cos", lambda: self.sci_func("cos"), "#6b5a8a"), ("tan", lambda: self.sci_func("tan"), "#6b5a8a"), ("π", lambda: self.append_to_expr(str(math.pi)), "#6b5a8a")],
            # Row 7
            [("√x", lambda: self.sci_func("sqrt"), "#6b5a8a"), ("x²", lambda: self.append_to_expr("**2"), "#6b5a8a"), ("x³", lambda: self.append_to_expr("**3"), "#6b5a8a"), ("e", lambda: self.append_to_expr(str(math.e)), "#6b5a8a")],
            # Row 8
            [("ln", lambda: self.sci_func("ln"), "#6b5a8a"), ("log", lambda: self.sci_func("log"), "#6b5a8a"), ("!", lambda: self.sci_func("factorial"), "#6b5a8a"), ("1/x", lambda: self.sci_func("reciprocal"), "#6b5a8a")],
        ]
        
        # Configure rows for equal weight
        for row_idx in range(len(buttons) + 1):
            calc_frame.grid_rowconfigure(row_idx, weight=1)
        
        for row_idx, row in enumerate(buttons, start=1):
            for col_idx, (text, command, color) in enumerate(row):
                btn = ctk.CTkButton(
                    calc_frame,
                    text=text,
                    command=command,
                    font=ctk.CTkFont(size=12, weight="bold"),
                    height=40,
                    fg_color=color,
                    hover_color=self.darken_color(color),
                    corner_radius=5
                )
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=3, pady=3)
    
    def darken_color(self, hex_color):
        """Darken a hex color for hover effect"""
        try:
            hex_color = hex_color.lstrip('#').strip()
            if len(hex_color) != 6:
                return "#333333"
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            darkened = tuple(max(0, c-30) for c in rgb)
            return '#{:02x}{:02x}{:02x}'.format(*darkened)
        except:
            return "#333333"
    
    def append_to_expr(self, value):
        """Append value to expression"""
        if self.expression == "0":
            self.expression = str(value)
        else:
            self.expression += str(value)
        self.update_display()
    
    def update_display(self):
        """Update the display label"""
        self.display_label.configure(text=self.expression if self.expression else "0")
    
    def clear(self):
        """Clear the calculator"""
        self.expression = ""
        self.update_display()
    
    def backspace(self):
        """Remove last character"""
        self.expression = self.expression[:-1]
        if not self.expression:
            self.expression = ""
        self.update_display()
    
    def sci_func(self, func):
        """Apply scientific function"""
        try:
            if func == "sin":
                result = math.sin(math.radians(float(self.expression)))
                self.expression = str(result)
                self.update_display()
            elif func == "cos":
                result = math.cos(math.radians(float(self.expression)))
                self.expression = str(result)
                self.update_display()
            elif func == "tan":
                result = math.tan(math.radians(float(self.expression)))
                self.expression = str(result)
                self.update_display()
            elif func == "sqrt":
                result = math.sqrt(float(self.expression))
                self.expression = str(result)
                self.update_display()
            elif func == "ln":
                result = math.log(float(self.expression))
                self.expression = str(result)
                self.update_display()
            elif func == "log":
                result = math.log10(float(self.expression))
                self.expression = str(result)
                self.update_display()
            elif func == "factorial":
                result = math.factorial(int(float(self.expression)))
                self.expression = str(result)
                self.update_display()
            elif func == "reciprocal":
                result = 1 / float(self.expression)
                self.expression = str(result)
                self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid operation: {str(e)}")
    
    def calculate_expr(self):
        """Calculate the expression"""
        try:
            if not self.expression:
                return
            
            result = eval(self.expression)
            
            # Log to history
            self.save_callback(
                "Scientific Calculator",
                {"expression": self.expression},
                {"result": result}
            )
            
            self.expression = str(result)
            self.update_display()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid expression: {str(e)}")
