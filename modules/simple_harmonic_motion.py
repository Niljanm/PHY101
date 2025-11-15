"""
Simple Harmonic Motion Module
Oscillations and wave analysis
"""

import customtkinter as ctk
import numpy as np
from tkinter import messagebox
from utils.validators import safe_float
from utils.plotter import create_plot

class SimpleHarmonicMotionModule:
    def __init__(self, parent, save_callback):
        self.parent = parent
        self.save_callback = save_callback
        
        parent.grid_columnconfigure(0, weight=1, minsize=250)
        parent.grid_columnconfigure(1, weight=2)
        parent.grid_rowconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            parent,
            text="Simple Harmonic Motion Calculator",
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
            text="Oscillatory Motion",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10), padx=20)
        
        ctk.CTkLabel(
            input_frame,
            text="Analyze simple harmonic oscillations",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20)
        
        fields = [
            ("Amplitude (A) [m]:", "A"),
            ("Angular Frequency (ω) [rad/s]:", "omega"),
            ("Frequency (f) [Hz]:", "f"),
            ("Period (T) [s]:", "T"),
            ("Phase (φ) [rad]:", "phi")
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
            text="Calculate SHM",
            command=self.calculate,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20, padx=20, fill="x")
        
        info = ctk.CTkLabel(
            input_frame,
            text="x(t) = A × cos(ωt + φ)\nω = 2πf = 2π/T",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform SHM calculations"""
        try:
            A_str = self.entries['A'].get().strip()
            omega_str = self.entries['omega'].get().strip()
            f_str = self.entries['f'].get().strip()
            T_str = self.entries['T'].get().strip()
            phi_str = self.entries['phi'].get().strip()
            
            if not A_str:
                messagebox.showerror("Error", "Amplitude is required!")
                return
            
            A = safe_float(A_str, "Amplitude")
            phi = safe_float(phi_str, "Phase") if phi_str else 0
            
            if A <= 0:
                messagebox.showerror("Error", "Amplitude must be positive!")
                return
            
            # Calculate frequency components
            if omega_str:
                omega = safe_float(omega_str, "Angular frequency")
                f = omega / (2*np.pi)
                T = 1 / f
            elif f_str:
                f = safe_float(f_str, "Frequency")
                omega = 2 * np.pi * f
                T = 1 / f
            elif T_str:
                T = safe_float(T_str, "Period")
                f = 1 / T
                omega = 2 * np.pi / T
            else:
                messagebox.showerror("Error", "Provide at least one: ω, f, or T!")
                return
            
            # Calculate max velocity and acceleration
            v_max = A * omega
            a_max = A * omega**2
            
            steps = [
                "Given:",
                f"  A = {A:.2f} m",
                f"  φ = {phi:.2f} rad",
                "",
                "Calculated:",
                f"  ω = {omega:.2f} rad/s",
                f"  f = {f:.2f} Hz",
                f"  T = {T:.2f} s",
                "",
                "Motion Parameters:",
                f"  Max Velocity = {v_max:.2f} m/s",
                f"  Max Acceleration = {a_max:.2f} m/s²",
                "",
                "Equation: x(t) = {:.2f} × cos({:.2f}t + {:.2f})".format(A, omega, phi)
            ]
            
            self.display_results(steps, A, omega, T, phi)
            self.save_callback("SHM", {"A": A, "omega": omega, "phi": phi}, 
                             {"f": f, "T": T, "v_max": v_max, "a_max": a_max})
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, A, omega, T, phi):
        """Display results and oscillation plots"""
        for widget in self.output_frame.winfo_children():
            widget.destroy()
        
        self.output_frame.grid_columnconfigure(0, weight=1)
        
        steps_frame = ctk.CTkFrame(self.output_frame)
        steps_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=15)
        
        ctk.CTkLabel(steps_frame, text="Results", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5), padx=15, anchor="w")
        solution_text = ctk.CTkTextbox(steps_frame, height=180, font=ctk.CTkFont(family="Courier", size=10))
        solution_text.pack(pady=(0, 10), padx=15, fill="both", expand=True)
        solution_text.insert("1.0", "\n".join(steps))
        solution_text.configure(state="disabled")
        
        plot_frame = ctk.CTkFrame(self.output_frame)
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.output_frame.grid_rowconfigure(1, weight=1)
        
        fig = create_plot(plot_frame, figsize=(8, 6))
        
        # Generate time array for 2-3 periods
        t = np.linspace(0, 3*T, 300)
        x = A * np.cos(omega*t + phi)
        v = -A*omega * np.sin(omega*t + phi)
        
        # Displacement vs Time
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(t, x, 'b-', linewidth=2.5, label='Displacement', zorder=3)
        ax1.scatter([0], [A*np.cos(phi)], color='red', s=100, zorder=5, edgecolors='darkred', linewidth=2)
        ax1.axhline(y=A, color='green', linestyle='--', alpha=0.5, label=f'Amplitude = ±{A:.2f}m')
        ax1.axhline(y=-A, color='green', linestyle='--', alpha=0.5)
        ax1.fill_between(t, x, alpha=0.2, color='blue', zorder=1)
        ax1.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Displacement (m)', fontsize=11, fontweight='bold')
        ax1.set_title('Simple Harmonic Motion - Displacement', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.4, linestyle='--')
        ax1.legend(fontsize=10, loc='best')
        
        # Velocity vs Time
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(t, v, 'r-', linewidth=2.5, label='Velocity', zorder=3)
        ax2.fill_between(t, v, alpha=0.2, color='red', zorder=1)
        ax2.axhline(y=A*omega, color='orange', linestyle='--', alpha=0.5, label=f'Max Velocity = ±{A*omega:.2f}m/s')
        ax2.axhline(y=-A*omega, color='orange', linestyle='--', alpha=0.5)
        ax2.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Velocity (m/s)', fontsize=11, fontweight='bold')
        ax2.set_title('Simple Harmonic Motion - Velocity', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.4, linestyle='--')
        ax2.legend(fontsize=10, loc='best')
        
        fig.tight_layout()
