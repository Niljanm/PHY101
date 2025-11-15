"""
Electrostatics Module
Coulomb's Law and electric field calculations
"""

import customtkinter as ctk
import numpy as np
from tkinter import messagebox
from utils.validators import safe_float
from utils.plotter import create_plot

class ElectrostaticsModule:
    def __init__(self, parent, save_callback):
        self.parent = parent
        self.save_callback = save_callback
        
        parent.grid_columnconfigure(0, weight=1, minsize=250)
        parent.grid_columnconfigure(1, weight=2)
        parent.grid_rowconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            parent,
            text="Electrostatics Calculator",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 15), sticky="w", padx=15)
        
        container = ctk.CTkFrame(parent)
        container.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=15, pady=(0, 15))
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=2)
        container.grid_rowconfigure(0, weight=1)
        
        self.create_input_frame(container)
        self.output_frame = ctk.CTkFrame(container)
        self.output_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        
    def create_input_frame(self, parent):
        """Create input controls"""
        input_frame = ctk.CTkFrame(parent)
        input_frame.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(
            input_frame,
            text="Coulomb's Law",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10), padx=20)
        
        ctk.CTkLabel(
            input_frame,
            text="Calculate electrostatic forces and fields",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20)
        
        fields = [
            ("Charge 1 (q₁) [C]:", "q1"),
            ("Charge 2 (q₂) [C]:", "q2"),
            ("Distance (r) [m]:", "r"),
            ("Electric Field (E) [N/C]:", "E"),
            ("Test Charge (q) [C]:", "q_test")
        ]
        
        self.entries = {}
        for label_text, key in fields:
            frame = ctk.CTkFrame(input_frame, fg_color="transparent")
            frame.pack(pady=8, padx=20, fill="x")
            
            ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=12)).pack(anchor="w")
            entry = ctk.CTkEntry(frame, placeholder_text="Enter value or leave blank")
            entry.pack(fill="x", pady=(5, 0))
            self.entries[key] = entry
        
        ctk.CTkButton(
            input_frame,
            text="Calculate Force",
            command=self.calculate,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20, padx=20, fill="x")
        
        info = ctk.CTkLabel(
            input_frame,
            text="k = 8.99 × 10⁹ N·m²/C²\nF = k × q₁ × q₂ / r²",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform electrostatics calculations"""
        try:
            q1_str = self.entries['q1'].get().strip()
            q2_str = self.entries['q2'].get().strip()
            r_str = self.entries['r'].get().strip()
            
            if not q1_str or not q2_str or not r_str:
                messagebox.showerror("Error", "Charge values and distance are required!")
                return
            
            q1 = safe_float(q1_str, "Charge 1")
            q2 = safe_float(q2_str, "Charge 2")
            r = safe_float(r_str, "Distance")
            
            if r <= 0:
                messagebox.showerror("Error", "Distance must be positive!")
                return
            
            k = 8.99e9  # Coulomb's constant
            
            # Calculate force
            F = k * abs(q1 * q2) / (r**2)
            
            # Force is repulsive if same sign, attractive if opposite
            force_type = "Repulsive" if (q1*q2) > 0 else "Attractive"
            
            # Electric field from q1
            E = k * abs(q1) / (r**2)
            
            steps = [
                "Given:",
                f"  q₁ = {q1:.2e} C",
                f"  q₂ = {q2:.2e} C",
                f"  r = {r:.2f} m",
                f"  k = 8.99 × 10⁹ N·m²/C²",
                "",
                "Coulomb's Law:",
                f"  F = k × |q₁ × q₂| / r²",
                f"  F = {F:.2e} N",
                "",
                f"Force Type: {force_type}",
                "",
                "Electric Field (from q₁):",
                f"  E = k × |q₁| / r²",
                f"  E = {E:.2e} N/C"
            ]
            
            self.display_results(steps, r, F, E)
            self.save_callback("Electrostatics", {"q1": q1, "q2": q2, "r": r}, 
                             {"F": F, "force_type": force_type, "E": E})
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, r, F, E):
        """Display results and force diagram"""
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        
        self.output_frame.grid_columnconfigure(0, weight=1)
        
        steps_frame = ctk.CTkFrame(self.output_frame)
        steps_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        
        ctk.CTkLabel(steps_frame, text="Results", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5), padx=15, anchor="w")
        solution_text = ctk.CTkTextbox(steps_frame, height=200, font=ctk.CTkFont(family="Courier", size=10))
        solution_text.pack(pady=(0, 10), padx=15, fill="both", expand=True)
        solution_text.insert("1.0", "\n".join(steps))
        solution_text.configure(state="disabled")
        
        plot_frame = ctk.CTkFrame(self.output_frame)
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.output_frame.grid_rowconfigure(1, weight=1)
        
        fig = create_plot(plot_frame, figsize=(8, 6))
        
        # Force vs Distance
        ax1 = fig.add_subplot(2, 1, 1)
        r_range = np.linspace(0.1*r, 3*r, 200)
        F_range = (F / (r**2)) * (r_range**-2)
        
        ax1.plot(r_range, F_range, 'r-', linewidth=2.5, label='F = k·q₁·q₂/r²', zorder=3)
        ax1.scatter([r], [F], color='red', s=120, zorder=5, edgecolors='darkred', linewidth=2)
        ax1.fill_between(r_range, F_range, alpha=0.2, color='red', zorder=1)
        ax1.axvline(x=r, color='red', linestyle='--', alpha=0.3, linewidth=1)
        ax1.set_xlabel('Distance (m)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Force (N)', fontsize=11, fontweight='bold')
        ax1.set_title('Electrostatic Force vs Distance', fontsize=12, fontweight='bold')
        ax1.set_yscale('log')
        ax1.grid(True, alpha=0.4, linestyle='--', which='both')
        ax1.legend(fontsize=10, loc='best')
        
        # Electric Field vs Distance
        ax2 = fig.add_subplot(2, 1, 2)
        E_range = (E / (r**2)) * (r_range**-2)
        
        ax2.plot(r_range, E_range, 'b-', linewidth=2.5, label='E = k·q/r²', zorder=3)
        ax2.scatter([r], [E], color='blue', s=120, zorder=5, edgecolors='darkblue', linewidth=2)
        ax2.fill_between(r_range, E_range, alpha=0.2, color='blue', zorder=1)
        ax2.axvline(x=r, color='blue', linestyle='--', alpha=0.3, linewidth=1)
        ax2.set_xlabel('Distance (m)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Electric Field (N/C)', fontsize=11, fontweight='bold')
        ax2.set_title('Electric Field vs Distance', fontsize=12, fontweight='bold')
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.4, linestyle='--', which='both')
        ax2.legend(fontsize=10, loc='best')
        
        fig.tight_layout()
