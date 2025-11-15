"""
Thermodynamics Module
Heat, temperature, and energy transfer calculations
"""

import customtkinter as ctk
import numpy as np
from tkinter import messagebox
from utils.validators import safe_float
from utils.plotter import create_plot

class ThermodynamicsModule:
    def __init__(self, parent, save_callback):
        self.parent = parent
        self.save_callback = save_callback
        
        # Configure parent grid with responsive weights
        parent.grid_columnconfigure(0, weight=1, minsize=250)
        parent.grid_columnconfigure(1, weight=2)
        parent.grid_rowconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            parent,
            text="Thermodynamics Calculator",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="w", padx=15)
        
        # Main container
        container = ctk.CTkFrame(parent)
        container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(0, 15))
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)
        
        # Input frame
        self.create_input_frame(container)
        
        # Output frame
        self.output_frame = ctk.CTkFrame(container)
        self.output_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
    def create_input_frame(self, parent):
        """Create input controls"""
        input_frame = ctk.CTkFrame(parent)
        input_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        ctk.CTkLabel(
            input_frame,
            text="Heat & Temperature",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10), padx=20)
        
        # Info
        ctk.CTkLabel(
            input_frame,
            text="Calculate heat transfer and temperature changes",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20)
        
        # Input fields
        fields = [
            ("Mass (m) [kg]:", "m"),
            ("Specific Heat Capacity (c) [J/kg·K]:", "c"),
            ("Temperature Change (ΔT) [K]:", "delta_t"),
            ("Initial Temperature (T₁) [°C]:", "t1"),
            ("Final Temperature (T₂) [°C]:", "t2")
        ]
        
        self.entries = {}
        for label_text, key in fields:
            frame = ctk.CTkFrame(input_frame, fg_color="transparent")
            frame.pack(pady=8, padx=20, fill="x")
            
            ctk.CTkLabel(
                frame,
                text=label_text,
                font=ctk.CTkFont(size=12)
            ).pack(anchor="w")
            
            entry = ctk.CTkEntry(frame, placeholder_text="Enter value")
            entry.pack(fill="x", pady=(5, 0))
            self.entries[key] = entry
        
        # Calculate button
        ctk.CTkButton(
            input_frame,
            text="Calculate Heat Transfer",
            command=self.calculate,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20, padx=20, fill="x")
        
        # Info
        info = ctk.CTkLabel(
            input_frame,
            text="Equation used:\nQ = m × c × ΔT\n\nWhere Q is heat energy (J)",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform thermodynamics calculations"""
        try:
            # Get inputs
            m_str = self.entries['m'].get().strip()
            c_str = self.entries['c'].get().strip()
            delta_t_str = self.entries['delta_t'].get().strip()
            t1_str = self.entries['t1'].get().strip()
            t2_str = self.entries['t2'].get().strip()
            
            # Validate inputs
            if not m_str or not c_str:
                messagebox.showerror("Error", "Mass and specific heat capacity are required!")
                return
            
            m = safe_float(m_str, "Mass")
            c = safe_float(c_str, "Specific heat capacity")
            
            if m <= 0 or c <= 0:
                messagebox.showerror("Error", "Mass and heat capacity must be positive!")
                return
            
            # Calculate temperature change if not provided
            if delta_t_str:
                delta_t = safe_float(delta_t_str, "Temperature change")
            elif t1_str and t2_str:
                t1 = safe_float(t1_str, "Initial temperature")
                t2 = safe_float(t2_str, "Final temperature")
                delta_t = t2 - t1
            else:
                messagebox.showerror("Error", "Provide either ΔT or both T₁ and T₂!")
                return
            
            # Calculate heat transfer
            Q = m * c * delta_t
            
            # Build solution steps
            steps = [
                "Given:",
                f"  m = {m} kg",
                f"  c = {c} J/kg·K",
                f"  ΔT = {delta_t} K",
                "",
                "Formula: Q = m × c × ΔT",
                "",
                "Calculation:",
                f"  Q = {m} × {c} × {delta_t}",
                f"  Q = {Q:.2f} J",
                f"  Q = {Q/1000:.2f} kJ"
            ]
            
            # Display results
            self.display_results(steps, m, c, delta_t, Q)
            
            # Save to history
            self.save_callback(
                "Thermodynamics",
                {"m": m, "c": c, "delta_t": delta_t},
                {"Q": Q}
            )
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, m, c, delta_t, Q):
        """Display calculation results and plots"""
        # Clear previous results
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        
        self.output_frame.grid_columnconfigure(0, weight=1)
        
        # Solution steps
        steps_frame = ctk.CTkFrame(self.output_frame)
        steps_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        
        ctk.CTkLabel(
            steps_frame,
            text="Step-by-Step Solution",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5), padx=15, anchor="w")
        
        solution_text = ctk.CTkTextbox(steps_frame, height=180, font=ctk.CTkFont(family="Courier", size=10))
        solution_text.pack(pady=(0, 10), padx=15, fill="both", expand=True)
        solution_text.insert("1.0", "\n".join(steps))
        solution_text.configure(state="disabled")
        
        # Create plots
        plot_frame = ctk.CTkFrame(self.output_frame)
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.output_frame.grid_rowconfigure(1, weight=1)
        
        # Create subplots
        fig = create_plot(plot_frame, figsize=(8, 6))
        
        # Heat vs Temperature Change
        ax1 = fig.add_subplot(2, 1, 1)
        temp_range = np.linspace(-delta_t, delta_t*2, 100)
        heat_range = m * c * temp_range
        
        ax1.plot(temp_range, heat_range, 'r-', linewidth=2.5, label='Q = m × c × ΔT', zorder=3)
        ax1.scatter([delta_t], [Q], color='red', s=120, zorder=5, edgecolors='darkred', linewidth=2)
        ax1.axhline(y=Q, color='red', linestyle='--', alpha=0.3, linewidth=1)
        ax1.axvline(x=delta_t, color='red', linestyle='--', alpha=0.3, linewidth=1)
        ax1.fill_between(temp_range, heat_range, alpha=0.2, color='red', zorder=1)
        ax1.set_xlabel('Temperature Change (K)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Heat Transfer (J)', fontsize=11, fontweight='bold')
        ax1.set_title('Heat Transfer vs Temperature Change', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.4, linestyle='--')
        ax1.legend(fontsize=10, loc='best')
        
        ax1.annotate(f'ΔT={delta_t:.2f}K, Q={Q:.0f}J', 
                    xy=(delta_t, Q), xytext=(delta_t*0.5, Q*0.8),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=9, color='red', fontweight='bold')
        
        # Heat vs Mass (with constant c and ΔT)
        ax2 = fig.add_subplot(2, 1, 2)
        mass_range = np.linspace(0.1, m*3, 100)
        heat_mass = mass_range * c * delta_t
        
        ax2.plot(mass_range, heat_mass, 'b-', linewidth=2.5, label='Q varies with mass', zorder=3)
        ax2.scatter([m], [Q], color='blue', s=120, zorder=5, edgecolors='darkblue', linewidth=2)
        ax2.fill_between(mass_range, heat_mass, alpha=0.2, color='blue', zorder=1)
        ax2.axhline(y=Q, color='blue', linestyle='--', alpha=0.3, linewidth=1)
        ax2.axvline(x=m, color='blue', linestyle='--', alpha=0.3, linewidth=1)
        ax2.set_xlabel('Mass (kg)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Heat Transfer (J)', fontsize=11, fontweight='bold')
        ax2.set_title('Heat Transfer vs Mass', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.4, linestyle='--')
        ax2.legend(fontsize=10, loc='best')
        
        ax2.annotate(f'm={m:.2f}kg, Q={Q:.0f}J', 
                    xy=(m, Q), xytext=(m*0.6, Q*0.7),
                    arrowprops=dict(arrowstyle='->', color='blue', lw=1.5),
                    fontsize=9, color='blue', fontweight='bold')
        
        fig.tight_layout()
