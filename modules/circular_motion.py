"""
Circular Motion Module
Centripetal force, angular velocity, and orbital mechanics
"""

import customtkinter as ctk
import numpy as np
from tkinter import messagebox
from utils.validators import safe_float
from utils.plotter import create_plot

class CircularMotionModule:
    def __init__(self, parent, save_callback):
        self.parent = parent
        self.save_callback = save_callback
        
        parent.grid_columnconfigure(0, weight=1, minsize=250)
        parent.grid_columnconfigure(1, weight=2)
        parent.grid_rowconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            parent,
            text="Circular Motion Calculator",
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
            text="Centripetal Motion",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10), padx=20)
        
        ctk.CTkLabel(
            input_frame,
            text="Calculate forces and motion in circular paths",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20)
        
        fields = [
            ("Mass (m) [kg]:", "m"),
            ("Radius (r) [m]:", "r"),
            ("Velocity (v) [m/s]:", "v"),
            ("Angular Velocity (ω) [rad/s]:", "omega"),
            ("Period (T) [s]:", "T")
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
            text="Calculate",
            command=self.calculate,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20, padx=20, fill="x")
        
        info = ctk.CTkLabel(
            input_frame,
            text="Equations:\nFc = m × v² / r\nω = v / r\nT = 2π / ω",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform circular motion calculations"""
        try:
            m_str = self.entries['m'].get().strip()
            r_str = self.entries['r'].get().strip()
            v_str = self.entries['v'].get().strip()
            omega_str = self.entries['omega'].get().strip()
            T_str = self.entries['T'].get().strip()
            
            if not m_str or not r_str:
                messagebox.showerror("Error", "Mass and radius are required!")
                return
            
            m = safe_float(m_str, "Mass")
            r = safe_float(r_str, "Radius")
            
            if m <= 0 or r <= 0:
                messagebox.showerror("Error", "Mass and radius must be positive!")
                return
            
            # Solve for missing variable
            if v_str:
                v = safe_float(v_str, "Velocity")
                omega = v / r
                T = 2 * np.pi / omega
            elif omega_str:
                omega = safe_float(omega_str, "Angular velocity")
                v = omega * r
                T = 2 * np.pi / omega
            elif T_str:
                T = safe_float(T_str, "Period")
                omega = 2 * np.pi / T
                v = omega * r
            else:
                messagebox.showerror("Error", "Provide at least one: velocity, angular velocity, or period!")
                return
            
            Fc = m * v**2 / r
            ac = v**2 / r
            
            steps = [
                "Given:",
                f"  m = {m} kg",
                f"  r = {r} m",
                "",
                "Calculated:",
                f"  v = {v:.2f} m/s",
                f"  ω = {omega:.2f} rad/s",
                f"  T = {T:.2f} s",
                "",
                "Centripetal Acceleration:",
                f"  ac = v² / r = {ac:.2f} m/s²",
                "",
                "Centripetal Force:",
                f"  Fc = m × ac = {Fc:.2f} N"
            ]
            
            self.display_results(steps, r, v, omega, Fc)
            self.save_callback("Circular Motion", {"m": m, "r": r, "v": v}, {"Fc": Fc, "omega": omega, "T": T})
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, r, v, omega, Fc):
        """Display results and plots"""
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
        
        # Circular path visualization
        ax1 = fig.add_subplot(2, 1, 1)
        theta = np.linspace(0, 2*np.pi, 100)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        
        ax1.plot(x, y, 'b-', linewidth=2.5, label='Orbital path', zorder=3)
        ax1.scatter([r], [0], color='red', s=120, zorder=5, edgecolors='darkred', linewidth=2, label='Position')
        ax1.arrow(0, 0, r*0.9, 0, head_width=0.1*r, head_length=0.1*r, fc='green', ec='green', alpha=0.7)
        ax1.set_xlabel('x (m)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('y (m)', fontsize=11, fontweight='bold')
        ax1.set_title('Circular Motion Path (radius = {:.2f}m)'.format(r), fontsize=12, fontweight='bold')
        ax1.set_aspect('equal')
        ax1.grid(True, alpha=0.4, linestyle='--')
        ax1.legend(fontsize=10, loc='best')
        
        # Force vs Velocity
        ax2 = fig.add_subplot(2, 1, 2)
        v_range = np.linspace(0.1, v*2, 100)
        Fc_range = (Fc / (v**2)) * v_range**2
        
        ax2.plot(v_range, Fc_range, 'r-', linewidth=2.5, label='Fc = m·v²/r', zorder=3)
        ax2.scatter([v], [Fc], color='red', s=120, zorder=5, edgecolors='darkred', linewidth=2)
        ax2.fill_between(v_range, Fc_range, alpha=0.2, color='red', zorder=1)
        ax2.set_xlabel('Velocity (m/s)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Centripetal Force (N)', fontsize=11, fontweight='bold')
        ax2.set_title('Centripetal Force vs Velocity', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.4, linestyle='--')
        ax2.legend(fontsize=10, loc='best')
        
        fig.tight_layout()
