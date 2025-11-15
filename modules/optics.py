"""
Optics Module
Thin Lens equation calculations with ray diagram
"""

import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from utils.validators import safe_float
from utils.plotter import create_plot

class OpticsModule:
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
            text="Optics Calculator",
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
        
        ctk.CTkLabel(
            input_frame,
            text="Thin Lens Equation",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20)
        
        # Input fields
        fields = [
            ("Focal Length (f) [cm]:", "f"),
            ("Object Distance (u) [cm]:", "u"),
            ("Image Distance (v) [cm] (optional):", "v")
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
            text="Calculate",
            command=self.calculate,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=20, padx=20, fill="x")
        
        # Info
        info = ctk.CTkLabel(
            input_frame,
            text="Formulas:\n"
                 "Thin Lens Equation:\n"
                 "1/f = 1/u + 1/v\n"
                 "Magnification:\n"
                 "m = -v/u",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform optics calculations"""
        try:
            # Get inputs
            f = safe_float(self.entries['f'].get(), "Focal Length")
            u = safe_float(self.entries['u'].get(), "Object Distance")
            v_str = self.entries['v'].get().strip()
            
            if f == 0:
                messagebox.showerror("Error", "Focal length cannot be zero!")
                return
            if u <= 0:
                messagebox.showerror("Error", "Object distance must be positive!")
                return
            
            # Calculate image distance if not provided
            if v_str:
                v = safe_float(v_str, "Image Distance")
            else:
                # Using thin lens equation: 1/f = 1/u + 1/v
                v = (f * u) / (u - f)
            
            # Calculate magnification
            m = -v / u
            
            steps = []
            steps.append("Given:")
            steps.append(f"  f = {f} cm")
            steps.append(f"  u = {u} cm")
            steps.append("")
            steps.append("Using Thin Lens Equation:")
            steps.append("  1/f = 1/u + 1/v")
            steps.append(f"  1/{f} = 1/{u} + 1/v")
            steps.append("")
            steps.append("Calculating Image Distance:")
            steps.append(f"  v = (f × u) / (u - f)")
            steps.append(f"  v = ({f} × {u}) / ({u} - {f})")
            steps.append(f"  v = {v:.3f} cm")
            steps.append("")
            steps.append("Calculating Magnification:")
            steps.append("  m = -v/u")
            steps.append(f"  m = -{v:.3f}/{u}")
            steps.append(f"  m = {m:.3f}")
            
            if m > 0:
                steps.append("  (Virtual, Erect image)")
            else:
                steps.append("  (Real, Inverted image)")
            
            # Display results
            self.display_results(steps, f, u, v, m)
            
            # Save to history
            self.save_callback(
                "Optics",
                {"f": f, "u": u},
                {"v": v, "magnification": m}
            )
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except ZeroDivisionError:
            messagebox.showerror("Error", "Object distance equals focal length - Image at infinity!")
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, f, u, v, m):
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
        
        solution_text = ctk.CTkTextbox(steps_frame, height=200, font=ctk.CTkFont(family="Courier", size=10))
        solution_text.pack(pady=(0, 10), padx=15, fill="both", expand=True)
        solution_text.insert("1.0", "\n".join(steps))
        solution_text.configure(state="disabled")
        
        # Create plot
        plot_frame = ctk.CTkFrame(self.output_frame)
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.output_frame.grid_rowconfigure(1, weight=1)
        
        fig = create_plot(plot_frame, figsize=(10, 6))
        
        # Create two subplots: Lens diagram and Magnification curve
        ax1 = fig.add_subplot(1, 2, 1)
        ax2 = fig.add_subplot(1, 2, 2)
        
        # Lens diagram
        lens_height = 2
        ax1.set_xlim(-u-1, max(v, 2*f)+2)
        ax1.set_ylim(-lens_height-1, lens_height+1)
        
        # Draw lens
        ax1.plot([0, 0], [-lens_height, lens_height], 'k-', linewidth=3, zorder=3)
        
        # Draw focal points
        ax1.scatter([-f], [0], color='red', s=100, marker='x', linewidth=2.5, zorder=4, label='Focal Points')
        ax1.scatter([f], [0], color='red', s=100, marker='x', linewidth=2.5, zorder=4)
        
        # Draw object
        ax1.arrow(-u, 0, 0, 0.8, head_width=0.15, head_length=0.1, fc='blue', ec='blue', linewidth=2, zorder=5)
        ax1.scatter([-u], [0.8], color='blue', s=120, marker='o', edgecolors='darkblue', linewidth=2, zorder=5)
        
        # Draw image (if real)
        if v > 0:
            ax1.arrow(v, 0, 0, m*0.8, head_width=0.15, head_length=0.1, fc='green', ec='green', linewidth=2, zorder=5)
            ax1.scatter([v], [m*0.8], color='green', s=120, marker='s', edgecolors='darkgreen', linewidth=2, zorder=5)
        
        # Draw optical axis
        ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5, zorder=1)
        
        # Add labels with parameters
        ax1.text(-u, 1.2, f'Object\nu={u:.2f}cm', ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightblue', alpha=0.7))
        
        if v > 0:
            ax1.text(v, m*0.8+0.5, f'Image\nv={v:.2f}cm\nm={m:.2f}', ha='center', fontsize=9, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.4', facecolor='lightgreen', alpha=0.7))
        
        ax1.text(0, -lens_height-0.7, f'Lens\nf={f:.2f}cm', ha='center', fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='lightyellow', alpha=0.7))
        
        ax1.set_xlabel('Distance (cm)', fontsize=10, fontweight='bold')
        ax1.set_ylabel('Height (cm)', fontsize=10, fontweight='bold')
        ax1.set_title('Lens Diagram', fontsize=11, fontweight='bold')
        ax1.grid(True, alpha=0.3, linestyle='--')
        ax1.set_aspect('equal', adjustable='box')
        
        # Magnification vs Object Distance curve
        u_range = np.linspace(0.5, max(u*2, 2*f+2), 200)
        m_range = []
        
        for u_val in u_range:
            try:
                v_val = (f * u_val) / (u_val - f) if u_val != f else float('inf')
                if v_val > 0:
                    m_val = -v_val / u_val
                    m_range.append(m_val)
                else:
                    m_range.append(np.nan)
            except:
                m_range.append(np.nan)
        
        # Filter out inf and nan
        u_plot = u_range[~np.isnan(m_range)]
        m_plot = np.array(m_range)[~np.isnan(m_range)]
        
        # Plot magnification curve
        ax2.plot(u_plot, m_plot, 'b-', linewidth=2.5, label='Magnification', zorder=3)
        
        # Mark current operating point
        ax2.scatter([u], [m], color='red', s=150, marker='o', edgecolors='darkred', linewidth=2.5, zorder=5, label='Current')
        
        # Draw reference lines to operating point
        ax2.axvline(x=u, color='red', linestyle='--', alpha=0.5, linewidth=1.5, zorder=2)
        ax2.axhline(y=m, color='red', linestyle='--', alpha=0.5, linewidth=1.5, zorder=2)
        
        # Add annotation with arrow
        ax2.annotate(f'u={u:.2f}cm\nm={m:.2f}',
                    xy=(u, m), xytext=(u+0.5, m+0.5),
                    arrowprops=dict(arrowstyle='->', color='red', lw=2),
                    fontsize=10, color='red', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8))
        
        # Add focal point line
        if f > 0:
            ax2.axvline(x=f, color='orange', linestyle=':', alpha=0.7, linewidth=2, label=f'Focal Point (f={f:.2f}cm)')
        
        ax2.set_xlabel('Object Distance (cm)', fontsize=10, fontweight='bold')
        ax2.set_ylabel('Magnification', fontsize=10, fontweight='bold')
        ax2.set_title('Magnification vs Object Distance', fontsize=11, fontweight='bold')
        ax2.grid(True, alpha=0.3, linestyle='--')
        ax2.minorticks_on()
        ax2.grid(True, which='minor', alpha=0.15, linestyle=':')
        ax2.legend(fontsize=9, loc='best')
        
        fig.tight_layout()
