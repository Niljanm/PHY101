"""
Projectile Motion Module
Trajectory calculations and range analysis
"""

import customtkinter as ctk
import numpy as np
from tkinter import messagebox
from utils.validators import safe_float
from utils.plotter import create_plot

class ProjectileMotionModule:
    def __init__(self, parent, save_callback):
        self.parent = parent
        self.save_callback = save_callback
        
        parent.grid_columnconfigure(0, weight=1, minsize=250)
        parent.grid_columnconfigure(1, weight=2)
        parent.grid_rowconfigure(1, weight=1)
        
        title = ctk.CTkLabel(
            parent,
            text="Projectile Motion Calculator",
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
            text="Projectile Analysis",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10), padx=20)
        
        ctk.CTkLabel(
            input_frame,
            text="Calculate range, height, and flight time",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20)
        
        fields = [
            ("Initial Velocity (v₀) [m/s]:", "v0"),
            ("Launch Angle (θ) [degrees]:", "theta"),
            ("Initial Height (h₀) [m]:", "h0")
        ]
        
        self.entries = {}
        for label_text, key in fields:
            frame = ctk.CTkFrame(input_frame, fg_color="transparent")
            frame.pack(pady=8, padx=20, fill="x")
            
            ctk.CTkLabel(frame, text=label_text, font=ctk.CTkFont(size=12)).pack(anchor="w")
            entry = ctk.CTkEntry(frame, placeholder_text="Enter value")
            entry.pack(fill="x", pady=(5, 0))
            self.entries[key] = entry
        
        ctk.CTkButton(
            input_frame,
            text="Calculate Trajectory",
            command=self.calculate,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20, padx=20, fill="x")
        
        info = ctk.CTkLabel(
            input_frame,
            text="g = 9.8 m/s²\nRange = (v₀² × sin(2θ)) / g\nMax Height = (v₀² × sin²(θ)) / (2g)",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform projectile motion calculations"""
        try:
            v0_str = self.entries['v0'].get().strip()
            theta_str = self.entries['theta'].get().strip()
            h0_str = self.entries['h0'].get().strip()
            
            if not v0_str or not theta_str:
                messagebox.showerror("Error", "Initial velocity and angle are required!")
                return
            
            v0 = safe_float(v0_str, "Initial velocity")
            theta_deg = safe_float(theta_str, "Launch angle")
            h0 = safe_float(h0_str, "Initial height") if h0_str else 0
            
            if v0 <= 0:
                messagebox.showerror("Error", "Initial velocity must be positive!")
                return
            
            g = 9.8
            theta_rad = np.radians(theta_deg)
            
            v0x = v0 * np.cos(theta_rad)
            v0y = v0 * np.sin(theta_rad)
            
            # Calculate max height
            h_max = h0 + (v0y**2) / (2*g)
            t_max = v0y / g
            
            # Calculate range (time to hit ground)
            # h0 + v0y*t - 0.5*g*t² = 0
            a = -0.5 * g
            b = v0y
            c = h0
            discriminant = b**2 - 4*a*c
            
            if discriminant < 0:
                t_flight = 0
                range_dist = 0
            else:
                t_flight = (-b - np.sqrt(discriminant)) / (2*a)
                range_dist = v0x * t_flight
            
            steps = [
                "Given:",
                f"  v₀ = {v0:.2f} m/s",
                f"  θ = {theta_deg:.2f}°",
                f"  h₀ = {h0:.2f} m",
                f"  g = {g} m/s²",
                "",
                "Velocity Components:",
                f"  v₀ₓ = v₀ × cos(θ) = {v0x:.2f} m/s",
                f"  v₀ᵧ = v₀ × sin(θ) = {v0y:.2f} m/s",
                "",
                "Flight Analysis:",
                f"  Maximum Height = {h_max:.2f} m",
                f"  Time to Max Height = {t_max:.2f} s",
                f"  Total Flight Time = {t_flight:.2f} s",
                f"  Range = {range_dist:.2f} m"
            ]
            
            self.display_results(steps, v0x, v0y, h0, t_flight, g)
            self.save_callback("Projectile Motion", {"v0": v0, "theta": theta_deg, "h0": h0}, 
                             {"range": range_dist, "max_height": h_max, "flight_time": t_flight})
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, v0x, v0y, h0, t_flight, g):
        """Display results and trajectory plot"""
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
        ax = fig.add_subplot(1, 1, 1)
        
        # Calculate trajectory
        t = np.linspace(0, t_flight, 200)
        x = v0x * t
        y = h0 + v0y * t - 0.5 * g * t**2
        
        ax.plot(x, y, 'b-', linewidth=3, label='Trajectory', zorder=3)
        ax.scatter([0], [h0], color='green', s=120, zorder=5, edgecolors='darkgreen', linewidth=2, label='Launch')
        ax.scatter([v0x*t_flight], [0], color='red', s=120, zorder=5, edgecolors='darkred', linewidth=2, label='Landing')
        ax.fill_between(x, y, alpha=0.2, color='blue', zorder=1)
        ax.axhline(y=0, color='brown', linestyle='-', linewidth=2, alpha=0.5, label='Ground')
        
        ax.set_xlabel('Horizontal Distance (m)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Height (m)', fontsize=11, fontweight='bold')
        ax.set_title('Projectile Trajectory', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.4, linestyle='--')
        ax.legend(fontsize=10, loc='best')
        ax.set_ylim(bottom=-0.5)
        
        fig.tight_layout()
