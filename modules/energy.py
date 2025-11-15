"""
Energy Module
Kinetic Energy and Work calculations with visualization
"""

import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from utils.validators import safe_float
from utils.plotter import create_plot

class EnergyModule:
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
            text="Energy Calculator",
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
            text="Input Parameters",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10), padx=20)
        
        # Input fields
        fields = [
            ("Mass (m) [kg]:", "m"),
            ("Velocity (v) [m/s]:", "v"),
            ("Force (F) [N] (optional):", "F"),
            ("Distance (d) [m] (optional):", "d"),
            ("Time (t) [s] (optional):", "t")
        ]
        
        self.entries = {}
        for label_text, key in fields:
            frame = ctk.CTkFrame(input_frame, fg_color="transparent")
            frame.pack(pady=6, padx=20, fill="x")
            
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
            text="Calculate",
            command=self.calculate,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=15, padx=20, fill="x")
        
        # Info
        info = ctk.CTkLabel(
            input_frame,
            text="Formulas:\n"
                 "KE = ½mv²\n"
                 "W = F·d\n"
                 "P = W/t",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform energy calculations"""
        try:
            # Get required inputs
            m = safe_float(self.entries['m'].get(), "Mass")
            v = safe_float(self.entries['v'].get(), "Velocity")
            
            if m <= 0:
                messagebox.showerror("Error", "Mass must be positive!")
                return
            if v < 0:
                messagebox.showerror("Error", "Velocity cannot be negative!")
                return
            
            # Calculate Kinetic Energy
            KE = 0.5 * m * v * v
            
            steps = []
            steps.append("Given:")
            steps.append(f"  m = {m} kg")
            steps.append(f"  v = {v} m/s")
            steps.append("")
            steps.append("Calculating Kinetic Energy:")
            steps.append("  KE = ½mv²")
            steps.append(f"  KE = 0.5 × {m} × {v}²")
            steps.append(f"  KE = 0.5 × {m} × {v*v}")
            steps.append(f"  KE = {KE:.3f} Joules")
            
            outputs = {"KE": KE}
            
            # Optional Work calculation
            f_str = self.entries['F'].get().strip()
            d_str = self.entries['d'].get().strip()
            
            if f_str and d_str:
                F = safe_float(f_str, "Force")
                d = safe_float(d_str, "Distance")
                
                if F < 0 or d < 0:
                    messagebox.showwarning("Warning", "Force and Distance should be non-negative!")
                
                W = F * d
                steps.append("")
                steps.append("Calculating Work Done:")
                steps.append("  W = F × d")
                steps.append(f"  W = {F} × {d}")
                steps.append(f"  W = {W:.3f} Joules")
                outputs["W"] = W
                
                # Optional Power calculation
                t_str = self.entries['t'].get().strip()
                if t_str:
                    t = safe_float(t_str, "Time")
                    if t <= 0:
                        messagebox.showerror("Error", "Time must be positive!")
                        return
                    P = W / t
                    steps.append("")
                    steps.append("Calculating Power:")
                    steps.append("  P = W / t")
                    steps.append(f"  P = {W:.3f} / {t}")
                    steps.append(f"  P = {P:.3f} Watts")
                    outputs["P"] = P
            
            # Display results
            self.display_results(steps, m, v, KE)
            
            # Save to history
            inputs = {"m": m, "v": v}
            if f_str and d_str:
                inputs.update({"F": float(f_str), "d": float(d_str)})
            self.save_callback("Energy", inputs, outputs)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, m, v, KE):
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
        
        # Create plot
        plot_frame = ctk.CTkFrame(self.output_frame)
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.output_frame.grid_rowconfigure(1, weight=1)
        
        # Generate KE vs velocity curve
        velocity_array = np.linspace(0, v * 1.5, 100)
        KE_array = 0.5 * m * velocity_array**2
        
        fig = create_plot(plot_frame, figsize=(8, 6))
        ax = fig.add_subplot(1, 1, 1)
        
        # Plot the curve
        ax.plot(velocity_array, KE_array, 'purple', linewidth=2.5, label='KE = ½mv²', zorder=3)
        ax.fill_between(velocity_array, KE_array, alpha=0.2, color='purple', zorder=1, label='Energy Area')
        
        # Plot current state
        ax.scatter([v], [KE], color='red', s=150, zorder=5, edgecolors='darkred', linewidth=2.5, label='Current State')
        ax.scatter([0], [0], color='green', s=80, zorder=5, marker='s', edgecolors='darkgreen', linewidth=1.5, label='Rest State')
        
        # Add reference lines
        ax.axhline(y=KE, color='red', linestyle='--', alpha=0.4, linewidth=1.5)
        ax.axvline(x=v, color='red', linestyle='--', alpha=0.4, linewidth=1.5)
        
        # Add annotation with detailed info
        textstr = f'v = {v:.3f} m/s\nKE = {KE:.3f} J\nm = {m:.3f} kg'
        ax.annotate(textstr,
                   xy=(v, KE), xytext=(v-v*0.2, KE+KE*0.2),
                   arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                   fontsize=10, color='red', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))
        
        ax.set_xlabel('Velocity (m/s)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Kinetic Energy (J)', fontsize=11, fontweight='bold')
        ax.set_title(f'Kinetic Energy vs Velocity (mass = {m:.2f} kg)', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.4, linestyle='--')
        ax.legend(fontsize=10, loc='best')
        
        # Add minor gridlines
        ax.minorticks_on()
        ax.grid(True, which='minor', alpha=0.2, linestyle=':')
        
        fig.tight_layout()
