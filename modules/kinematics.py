"""
Kinematics Module
Equations of motion calculations with visualization
"""

import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from utils.validators import safe_float
from utils.plotter import create_plot

class KinematicsModule:
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
            text="Kinematics Calculator",
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
        
        # Info
        info = ctk.CTkLabel(
            input_frame,
            text="Enter any 3 values to solve for the 4th",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20)
        
        # Input fields
        fields = [
            ("Initial Velocity (u) [m/s]:", "u"),
            ("Final Velocity (v) [m/s]:", "v"),
            ("Acceleration (a) [m/s²]:", "a"),
            ("Time (t) [s]:", "t"),
            ("Displacement (s) [m]:", "s")
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
            
            entry = ctk.CTkEntry(frame, placeholder_text="Leave blank to calculate")
            entry.pack(fill="x", pady=(5, 0))
            self.entries[key] = entry
        
        # Calculate button
        ctk.CTkButton(
            input_frame,
            text="Calculate",
            command=self.calculate,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20, padx=20, fill="x")
        
        # Info
        info = ctk.CTkLabel(
            input_frame,
            text="Equations used:\n"
                 "v = u + at\n"
                 "s = ut + ½at²\n"
                 "v² = u² + 2as",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform kinematics calculations - solve for missing variable"""
        try:
            # Get inputs
            u_str = self.entries['u'].get().strip()
            v_str = self.entries['v'].get().strip()
            a_str = self.entries['a'].get().strip()
            t_str = self.entries['t'].get().strip()
            s_str = self.entries['s'].get().strip()
            
            # Count filled values
            filled_count = sum([bool(u_str), bool(v_str), bool(a_str), bool(t_str), bool(s_str)])
            
            if filled_count < 3:
                messagebox.showerror("Error", "Please enter at least 3 values!")
                return
            
            # Parse the values
            u = safe_float(u_str, "Initial velocity") if u_str else None
            v = safe_float(v_str, "Final velocity") if v_str else None
            a = safe_float(a_str, "Acceleration") if a_str else None
            t = safe_float(t_str, "Time") if t_str else None
            s = safe_float(s_str, "Displacement") if s_str else None
            
            steps = ["Given:"]
            outputs = {}
            
            # Solve for missing variable
            if u is None:  # Solve for u: u = v - at
                u = v - a * t
                steps.append(f"  v = {v} m/s")
                steps.append(f"  a = {a} m/s²")
                steps.append(f"  t = {t} s")
                steps.append("")
                steps.append("Solving for Initial Velocity:")
                steps.append("  v = u + at")
                steps.append("  u = v - at")
                steps.append(f"  u = {v} - {a}×{t}")
                steps.append(f"  u = {u:.3f} m/s")
                outputs['u'] = u
                
            elif v is None:  # Solve for v: v = u + at
                v = u + a * t
                steps.append(f"  u = {u} m/s")
                steps.append(f"  a = {a} m/s²")
                steps.append(f"  t = {t} s")
                steps.append("")
                steps.append("Solving for Final Velocity:")
                steps.append("  v = u + at")
                steps.append(f"  v = {u} + {a}×{t}")
                steps.append(f"  v = {v:.3f} m/s")
                outputs['v'] = v
                
            elif a is None:  # Solve for a: a = (v - u) / t
                if t == 0:
                    messagebox.showerror("Error", "Time cannot be zero!")
                    return
                a = (v - u) / t
                steps.append(f"  u = {u} m/s")
                steps.append(f"  v = {v} m/s")
                steps.append(f"  t = {t} s")
                steps.append("")
                steps.append("Solving for Acceleration:")
                steps.append("  v = u + at")
                steps.append("  a = (v - u) / t")
                steps.append(f"  a = ({v} - {u}) / {t}")
                steps.append(f"  a = {a:.3f} m/s²")
                outputs['a'] = a
                
            elif t is None:  # Solve for t: t = (v - u) / a
                if a == 0:
                    messagebox.showerror("Error", "Acceleration cannot be zero for this calculation!")
                    return
                t = (v - u) / a
                steps.append(f"  u = {u} m/s")
                steps.append(f"  v = {v} m/s")
                steps.append(f"  a = {a} m/s²")
                steps.append("")
                steps.append("Solving for Time:")
                steps.append("  v = u + at")
                steps.append("  t = (v - u) / a")
                steps.append(f"  t = ({v} - {u}) / {a}")
                steps.append(f"  t = {t:.3f} s")
                outputs['t'] = t
                
            else:  # s is None - Solve for s: s = ut + ½at² or s = (v² - u²) / 2a
                # Using: v² = u² + 2as => s = (v² - u²) / 2a
                if a == 0:
                    messagebox.showerror("Error", "Acceleration cannot be zero for this calculation!")
                    return
                s = (v*v - u*u) / (2 * a)
                steps.append(f"  u = {u} m/s")
                steps.append(f"  v = {v} m/s")
                steps.append(f"  a = {a} m/s²")
                steps.append(f"  t = {t} s")
                steps.append("")
                steps.append("Solving for Displacement:")
                steps.append("  v² = u² + 2as")
                steps.append("  s = (v² - u²) / 2a")
                steps.append(f"  s = ({v}² - {u}²) / (2×{a})")
                steps.append(f"  s = ({v*v:.3f} - {u*u:.3f}) / {2*a:.3f}")
                steps.append(f"  s = {s:.3f} m")
                outputs['s'] = s
            
            # Display results
            self.display_results(steps, u, v, a, t, s)
            
            # Save to history
            self.save_callback(
                "Kinematics",
                {"u": u, "v": v, "a": a, "t": t, "s": s},
                outputs
            )
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, u, v, a, t, s):
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
        
        # Generate time array
        time_array = np.linspace(0, t, 100)
        velocity_array = u + a * time_array
        displacement_array = u * time_array + 0.5 * a * time_array**2
        
        # Create subplot
        fig = create_plot(plot_frame, figsize=(8, 6))
        
        # Velocity vs Time
        ax1 = fig.add_subplot(2, 1, 1)
        ax1.plot(time_array, velocity_array, 'b-', linewidth=2.5, label='Velocity', zorder=3)
        ax1.scatter([t], [v], color='red', s=120, zorder=5, edgecolors='darkred', linewidth=2, label=f'Final: {v:.2f} m/s')
        ax1.scatter([0], [u], color='green', s=80, zorder=5, marker='s', edgecolors='darkgreen', linewidth=1.5, label=f'Initial: {u:.2f} m/s')
        ax1.axhline(y=v, color='red', linestyle='--', alpha=0.3, linewidth=1)
        ax1.axvline(x=t, color='red', linestyle='--', alpha=0.3, linewidth=1)
        ax1.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Velocity (m/s)', fontsize=11, fontweight='bold')
        ax1.set_title('Velocity vs Time', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.4, linestyle='--')
        ax1.legend(fontsize=10, loc='best')
        
        # Add annotation
        ax1.annotate(f'({t:.2f}s, {v:.2f}m/s)', 
                    xy=(t, v), xytext=(t-0.1, v+abs(a*t)*0.1),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=9, color='red', fontweight='bold')
        
        # Displacement vs Time
        ax2 = fig.add_subplot(2, 1, 2)
        ax2.plot(time_array, displacement_array, 'g-', linewidth=2.5, label='Displacement', zorder=3)
        ax2.fill_between(time_array, displacement_array, alpha=0.2, color='green', zorder=1)
        ax2.scatter([t], [s], color='red', s=120, zorder=5, edgecolors='darkred', linewidth=2, label=f'Final: {s:.2f} m')
        ax2.scatter([0], [0], color='green', s=80, zorder=5, marker='s', edgecolors='darkgreen', linewidth=1.5, label='Start: 0 m')
        ax2.axhline(y=s, color='red', linestyle='--', alpha=0.3, linewidth=1)
        ax2.axvline(x=t, color='red', linestyle='--', alpha=0.3, linewidth=1)
        ax2.set_xlabel('Time (s)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Displacement (m)', fontsize=11, fontweight='bold')
        ax2.set_title('Displacement vs Time', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.4, linestyle='--')
        ax2.legend(fontsize=10, loc='best')
        
        # Add annotation
        ax2.annotate(f'({t:.2f}s, {s:.2f}m)', 
                    xy=(t, s), xytext=(t-0.1, s+abs(s)*0.1),
                    arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                    fontsize=9, color='red', fontweight='bold')
        
        fig.tight_layout()
