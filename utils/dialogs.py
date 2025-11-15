"""
Dialog Windows and Popups
For history, help, formulas, and utilities
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from datetime import datetime
import json
from pathlib import Path
from utils.history import load_history


class HistoryViewerDialog:
    """Dialog to view and manage calculation history"""
    
    def __init__(self, parent, history_data):
        self.history_data = history_data
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Calculation History")
        self.dialog.geometry("700x500")
        self.dialog.grab_set()
        
        # Configure grid
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(1, weight=1)
        
        # Top frame for search
        top_frame = ctk.CTkFrame(self.dialog)
        top_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 10))
        top_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(top_frame, text="Search:", font=ctk.CTkFont(size=11)).pack(side="left", padx=(0, 10))
        self.search_var = ctk.StringVar()
        search_entry = ctk.CTkEntry(top_frame, textvariable=self.search_var, placeholder_text="Filter by module...")
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda e: self.filter_history())
        
        # Main content
        content_frame = ctk.CTkFrame(self.dialog)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_rowconfigure(0, weight=1)
        
        # Textbox with scrollbar
        self.text_widget = ctk.CTkTextbox(content_frame, font=ctk.CTkFont(family="Courier", size=9))
        self.text_widget.grid(row=0, column=0, sticky="nsew")
        self.text_widget.configure(state="disabled")
        
        # Display history
        self.display_history()
        
        # Bottom buttons
        btn_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        btn_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(10, 15))
        
        ctk.CTkButton(btn_frame, text="Clear All History", command=self.clear_history,
                     fg_color="#FF6B6B", hover_color="#CC5555").pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Export", command=self.export_history).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Close", command=self.dialog.destroy).pack(side="right", padx=5)
    
    def display_history(self):
        """Display calculation history"""
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        
        if not self.history_data:
            self.text_widget.insert("1.0", "No calculation history yet.")
            self.text_widget.configure(state="disabled")
            return
        
        # Show last 20 calculations, reversed (newest first)
        for calc in reversed(self.history_data[-20:]):
            timestamp = calc.get('timestamp', 'N/A')
            module = calc.get('module', 'Unknown')
            inputs = calc.get('inputs', {})
            outputs = calc.get('outputs', {})
            
            # Format the entry
            text = f"\n{'='*70}\n"
            text += f"[{timestamp}] {module}\n"
            text += f"{'-'*70}\n"
            text += "Inputs:\n"
            
            for key, val in inputs.items():
                if isinstance(val, float):
                    text += f"  {key}: {val:.4f}\n"
                else:
                    text += f"  {key}: {val}\n"
            
            text += "Outputs:\n"
            for key, val in outputs.items():
                if isinstance(val, float):
                    text += f"  {key}: {val:.4f}\n"
                else:
                    text += f"  {key}: {val}\n"
            
            self.text_widget.insert("end", text)
        
        self.text_widget.configure(state="disabled")
    
    def filter_history(self):
        """Filter history by search term"""
        search_term = self.search_var.get().lower()
        self.text_widget.configure(state="normal")
        self.text_widget.delete("1.0", "end")
        
        # Filter by module name
        if search_term:
            filtered = [c for c in self.history_data if search_term in c.get('module', '').lower()]
        else:
            filtered = self.history_data
        
        if not filtered:
            self.text_widget.insert("1.0", "No matching calculations found.")
            self.text_widget.configure(state="disabled")
            return
        
        # Display filtered results (newest first)
        for calc in reversed(filtered[-20:]):
            timestamp = calc.get('timestamp', 'N/A')
            module = calc.get('module', 'Unknown')
            inputs = calc.get('inputs', {})
            outputs = calc.get('outputs', {})
            
            # Format the entry
            text = f"\n{'='*70}\n"
            text += f"[{timestamp}] {module}\n"
            text += f"{'-'*70}\n"
            text += "Inputs:\n"
            
            for key, val in inputs.items():
                if isinstance(val, float):
                    text += f"  {key}: {val:.4f}\n"
                else:
                    text += f"  {key}: {val}\n"
            
            text += "Outputs:\n"
            for key, val in outputs.items():
                if isinstance(val, float):
                    text += f"  {key}: {val:.4f}\n"
                else:
                    text += f"  {key}: {val}\n"
            
            self.text_widget.insert("end", text)
        
        self.text_widget.configure(state="disabled")
    
    def clear_history(self):
        """Clear all history"""
        if messagebox.askyesno("Confirm", "Delete all calculation history?"):
            from utils.history import clear_all_history
            clear_all_history()
            # Reload the data
            self.history_data = []
            messagebox.showinfo("Success", "History cleared!")
            self.display_history()
    
    def export_history(self):
        """Export history to text file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w') as f:
                f.write("Physics Calculator History Export\n")
                f.write(f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")
                for calc in self.history_data:
                    f.write(f"[{calc.get('timestamp')}] {calc.get('module')}\n")
                    f.write(f"Input: {json.dumps(calc.get('inputs'), indent=2)}\n")
                    f.write(f"Output: {json.dumps(calc.get('outputs'), indent=2)}\n")
                    f.write("-" * 70 + "\n")
            messagebox.showinfo("Success", f"History exported to {file_path}")


class FormulasDialog:
    """Dialog showing physics formulas reference"""
    
    FORMULAS = {
        "Kinematics": [
            "v = u + at (Final velocity)",
            "s = ut + ½at² (Displacement)",
            "v² = u² + 2as (v² - u² = 2as)",
            "s = (u + v)t / 2 (Average velocity)",
            "a = (v - u) / t (Acceleration)"
        ],
        "Ohm's Law": [
            "V = IR (Ohm's Law)",
            "P = VI (Power)",
            "P = I²R (Power from current)",
            "R = ρL/A (Resistance)",
            "E = Pt (Energy)"
        ],
        "Energy": [
            "KE = ½mv² (Kinetic Energy)",
            "PE = mgh (Gravitational PE)",
            "ME = KE + PE (Mechanical Energy)",
            "W = F·d = ΔKE (Work-Energy)",
            "P = W/t (Power)"
        ],
        "Momentum": [
            "p = mv (Linear Momentum)",
            "F = Δp/Δt (Force & Impulse)",
            "J = FΔt = Δp (Impulse)",
            "p_total = Σp_i (Conservation)",
            "e = (v₂ - v₁)/(u₁ - u₂) (Coefficient of restitution)"
        ],
        "Optics": [
            "1/f = 1/u + 1/v (Thin Lens)",
            "m = -v/u (Magnification)",
            "f = R/2 (Mirror focal length)",
            "P = 1/f (Power of lens in diopters)",
            "sin(θ₁)/sin(θ₂) = n₂/n₁ (Snell's Law)"
        ],
        "Thermodynamics": [
            "Q = mcΔT (Heat transfer)",
            "ΔE = Q - W (1st Law)",
            "PV = nRT (Ideal Gas Law)",
            "η = W/Q_h (Efficiency)",
            "S = Q/T (Entropy)"
        ],
        "Circular Motion": [
            "v = ωr (Tangential velocity)",
            "a_c = v²/r = ω²r (Centripetal acceleration)",
            "F_c = mv²/r = mω²r (Centripetal force)",
            "T = 1/f = 2π/ω (Period & frequency)",
            "ω = 2πf (Angular velocity)"
        ],
        "Projectile Motion": [
            "x = v₀cos(θ)t (Horizontal range)",
            "y = v₀sin(θ)t - ½gt² (Vertical height)",
            "v_x = v₀cos(θ) (Horizontal velocity)",
            "v_y = v₀sin(θ) - gt (Vertical velocity)",
            "R = v₀²sin(2θ)/g (Max range)"
        ],
        "Simple Harmonic Motion": [
            "x = A sin(ωt + φ) (Displacement)",
            "v = Aω cos(ωt + φ) (Velocity)",
            "a = -Aω² sin(ωt + φ) (Acceleration)",
            "T = 2π√(m/k) (Period for spring)",
            "E = ½kA² (Total energy)"
        ],
        "Electrostatics": [
            "F = k|q₁q₂|/r² (Coulomb's Law)",
            "E = F/q = kQ/r² (Electric field)",
            "V = kQ/r (Electric potential)",
            "U = kq₁q₂/r (Potential energy)",
            "C = Q/V (Capacitance)"
        ],
        "Scientific Calculator": [
            "Basic: +, -, ×, ÷ (Arithmetic)",
            "Trig: sin(θ), cos(θ), tan(θ) (in degrees)",
            "Roots: √x, x² , x³ (Powers & roots)",
            "Log: ln(x), log₁₀(x) (Logarithms)",
            "Other: n!, 1/x, π, e (Functions & constants)"
        ]
    }
    
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Physics Formulas Reference")
        self.dialog.geometry("600x500")
        self.dialog.grab_set()
        
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(self.dialog, text="Physics Formulas Reference",
                            font=ctk.CTkFont(size=16, weight="bold"))
        title.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")
        
        # Textbox with formulas
        text_widget = ctk.CTkTextbox(self.dialog, font=ctk.CTkFont(family="Courier", size=10))
        text_widget.grid(row=1, column=0, sticky="nsew", padx=15, pady=10)
        
        content = "PHYSICS FORMULAS REFERENCE\n"
        content += "=" * 50 + "\n\n"
        
        for module, formulas in self.FORMULAS.items():
            content += f"{module.upper()}\n"
            content += "-" * 50 + "\n"
            for formula in formulas:
                content += f"  {formula}\n"
            content += "\n"
        
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")
        
        # Close button
        ctk.CTkButton(self.dialog, text="Close", command=self.dialog.destroy).grid(
            row=2, column=0, sticky="e", padx=15, pady=(10, 15)
        )


class HelpDialog:
    """Help and about dialog"""
    
    def __init__(self, parent):
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Help & About")
        self.dialog.geometry("550x600")
        self.dialog.grab_set()
        
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(0, weight=1)
        
        # Textbox with help content
        text_widget = ctk.CTkTextbox(self.dialog, font=ctk.CTkFont(size=10))
        text_widget.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        
        help_text = """PHYSICS CALCULATOR & VISUALIZER
Version 1.5

FEATURES:
• Multi-module physics calculator with 5 core modules
• Interactive 2D/3D graph visualizations
• Automatic calculation history saving
• Real-time result updates
• Responsive design for all screen sizes
• Dark/Light theme support

MODULES:
1. Kinematics - Motion analysis with flexible solving
2. Ohm's Law - Electrical circuits and resistance
3. Energy - Kinetic and potential energy calculations
4. Momentum - Collision and momentum analysis
5. Optics - Thin lens and ray diagram calculations

HOW TO USE:
1. Select a module from the left sidebar
2. Enter the required parameters
3. Click "Calculate" to solve
4. View step-by-step solution and graphs
5. Results are automatically saved to history

KEYBOARD SHORTCUTS:
Ctrl+K - Kinematics
Ctrl+O - Ohm's Law
Ctrl+E - Energy
Ctrl+M - Momentum
Ctrl+P - Optics
Ctrl+H - View History

TIPS:
• Hover over input fields for hints
• Click "Reset" to clear inputs
• Use "Copy Results" to export calculations
• View History to track previous calculations
• Use Unit Converter to switch between units

SUPPORT:
For issues or suggestions, check the Help menu.

Created with CustomTkinter, NumPy, and Matplotlib
"""
        text_widget.insert("1.0", help_text)
        text_widget.configure(state="disabled")
        
        # Close button
        ctk.CTkButton(self.dialog, text="Close", command=self.dialog.destroy).grid(
            row=1, column=0, sticky="e", padx=15, pady=(10, 15)
        )


class UnitConverterDialog:
    """Unit conversion utility dialog"""
    
    def __init__(self, parent):
        from utils.unit_converter import UnitConverter
        
        self.converter = UnitConverter
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("Unit Converter")
        self.dialog.geometry("500x400")
        self.dialog.grab_set()
        
        self.dialog.grid_columnconfigure(0, weight=1)
        self.dialog.grid_rowconfigure(2, weight=1)
        
        # Title
        title = ctk.CTkLabel(self.dialog, text="Unit Converter",
                            font=ctk.CTkFont(size=16, weight="bold"))
        title.grid(row=0, column=0, columnspan=3, padx=15, pady=(15, 20))
        
        # Conversion type selector
        type_frame = ctk.CTkFrame(self.dialog, fg_color="transparent")
        type_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=15, pady=10)
        type_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(type_frame, text="Convert:", font=ctk.CTkFont(size=11)).pack(side="left", padx=(0, 10))
        
        self.type_var = ctk.StringVar(value="Speed")
        type_menu = ctk.CTkComboBox(type_frame, values=["Speed", "Mass", "Distance", "Energy", "Voltage"],
                                   variable=self.type_var, command=self.update_units)
        type_menu.pack(side="left", fill="x", expand=True)
        
        # Conversion inputs
        content_frame = ctk.CTkFrame(self.dialog)
        content_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=15, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # From value
        ctk.CTkLabel(content_frame, text="From:", font=ctk.CTkFont(size=11)).grid(row=0, column=0, sticky="w", pady=5)
        self.from_value = ctk.CTkEntry(content_frame, placeholder_text="Enter value")
        self.from_value.grid(row=0, column=1, sticky="ew", padx=(10, 5), pady=5)
        self.from_unit = ctk.CTkComboBox(content_frame, values=["m/s", "km/h", "mph"], width=80)
        self.from_unit.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # To value
        ctk.CTkLabel(content_frame, text="To:", font=ctk.CTkFont(size=11)).grid(row=1, column=0, sticky="w", pady=5)
        self.to_value = ctk.CTkEntry(content_frame, state="readonly", placeholder_text="Result")
        self.to_value.grid(row=1, column=1, sticky="ew", padx=(10, 5), pady=5)
        self.to_unit = ctk.CTkComboBox(content_frame, values=["m/s", "km/h", "mph"], width=80)
        self.to_unit.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        self.from_value.bind("<KeyRelease>", lambda e: self.convert_units())
        
        # Convert button
        ctk.CTkButton(self.dialog, text="Convert", command=self.convert_units).grid(
            row=3, column=0, columnspan=3, sticky="ew", padx=15, pady=(10, 15)
        )
    
    def update_units(self, *args):
        """Update unit options based on conversion type"""
        conv_type = self.type_var.get()
        
        units_map = {
            "Speed": ["m/s", "km/h", "mph", "ft/s", "knots"],
            "Mass": ["kg", "g", "mg", "lb", "oz"],
            "Distance": ["m", "cm", "mm", "km", "ft", "in", "mile"],
            "Energy": ["J", "kJ", "MJ", "cal", "kcal"],
            "Voltage": ["V", "kV", "mV", "μV"]
        }
        
        units = units_map.get(conv_type, [])
        self.from_unit.configure(values=units)
        self.to_unit.configure(values=units)
        self.from_unit.set(units[0] if units else "")
        self.to_unit.set(units[1] if len(units) > 1 else units[0])
    
    def convert_units(self):
        """Perform unit conversion"""
        try:
            value = float(self.from_value.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            conv_type = self.type_var.get()
            
            if conv_type == "Speed":
                result = self.converter.convert_speed(value, from_unit, to_unit)
            elif conv_type == "Mass":
                result = self.converter.convert_mass(value, from_unit, to_unit)
            elif conv_type == "Distance":
                result = self.converter.convert_distance(value, from_unit, to_unit)
            elif conv_type == "Energy":
                result = self.converter.convert_energy(value, from_unit, to_unit)
            elif conv_type == "Voltage":
                result = self.converter.convert_voltage(value, from_unit, to_unit)
            
            self.to_value.configure(state="normal")
            self.to_value.delete(0, "end")
            self.to_value.insert(0, f"{result:.6f}")
            self.to_value.configure(state="readonly")
        except ValueError:
            self.to_value.configure(state="normal")
            self.to_value.delete(0, "end")
            self.to_value.insert(0, "Invalid input")
            self.to_value.configure(state="readonly")
