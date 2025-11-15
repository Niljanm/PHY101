"""
Momentum Module
Collision calculations with visualization
"""

import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from utils.validators import safe_float
from utils.plotter import create_plot

class MomentumModule:
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
            text="Momentum Calculator",
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
            ("Mass 1 (m₁) [kg]:", "m1"),
            ("Velocity 1 (v₁) [m/s]:", "v1"),
            ("Mass 2 (m₂) [kg]:", "m2"),
            ("Velocity 2 (v₂) [m/s]:", "v2")
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
                 "p = m × v\n"
                 "Conservation of Momentum:\n"
                 "m₁v₁ + m₂v₂ = m₁v₁' + m₂v₂'",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform momentum calculations"""
        try:
            # Get inputs
            m1 = safe_float(self.entries['m1'].get(), "Mass 1")
            v1 = safe_float(self.entries['v1'].get(), "Velocity 1")
            m2 = safe_float(self.entries['m2'].get(), "Mass 2")
            v2 = safe_float(self.entries['v2'].get(), "Velocity 2")
            
            if m1 <= 0 or m2 <= 0:
                messagebox.showerror("Error", "Masses must be positive!")
                return
            
            # Calculate momentum
            p1 = m1 * v1
            p2 = m2 * v2
            p_total = p1 + p2
            
            steps = []
            steps.append("Given:")
            steps.append(f"  m₁ = {m1} kg")
            steps.append(f"  v₁ = {v1} m/s")
            steps.append(f"  m₂ = {m2} kg")
            steps.append(f"  v₂ = {v2} m/s")
            steps.append("")
            steps.append("Calculating Individual Momenta:")
            steps.append("  p₁ = m₁ × v₁")
            steps.append(f"  p₁ = {m1} × {v1} = {p1:.3f} kg·m/s")
            steps.append("")
            steps.append("  p₂ = m₂ × v₂")
            steps.append(f"  p₂ = {m2} × {v2} = {p2:.3f} kg·m/s")
            steps.append("")
            steps.append("Total Momentum (Conservation):")
            steps.append(f"  p_total = p₁ + p₂")
            steps.append(f"  p_total = {p1:.3f} + {p2:.3f}")
            steps.append(f"  p_total = {p_total:.3f} kg·m/s")
            
            # Display results
            self.display_results(steps, m1, v1, m2, v2, p1, p2, p_total)
            
            # Save to history
            self.save_callback(
                "Momentum",
                {"m1": m1, "v1": v1, "m2": m2, "v2": v2},
                {"p1": p1, "p2": p2, "p_total": p_total}
            )
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, m1, v1, m2, v2, p1, p2, p_total):
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
        
        fig = create_plot(plot_frame, figsize=(8, 6))
        
        # Create two subplots
        ax1 = fig.add_subplot(2, 1, 1)
        ax2 = fig.add_subplot(2, 1, 2)
        
        # Individual momenta bar chart
        objects1 = ['Object 1', 'Object 2']
        momenta1 = [p1, p2]
        colors1 = ['#1f77b4', '#ff7f0e']
        
        bars1 = ax1.bar(objects1, momenta1, color=colors1, alpha=0.8, edgecolor='black', linewidth=2, zorder=3)
        
        # Add value labels on bars
        for bar, value in zip(bars1, momenta1):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Add data labels
        ax1.text(0, p1, f'm₁={m1:.2f}kg\nv₁={v1:.2f}m/s', ha='center', va='top', fontsize=9, 
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightblue', alpha=0.5))
        ax1.text(1, p2, f'm₂={m2:.2f}kg\nv₂={v2:.2f}m/s', ha='center', va='top', fontsize=9,
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', alpha=0.5))
        
        ax1.set_ylabel('Momentum (kg·m/s)', fontsize=11, fontweight='bold')
        ax1.set_title('Individual Momenta', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax1.set_ylim(0, max(p1, p2) * 1.3)
        
        # Total momentum visualization
        objects2 = ['Object 1', 'Object 2', 'Total']
        momenta2 = [p1, p2, p_total]
        colors2 = ['#1f77b4', '#ff7f0e', '#2ca02c']
        
        bars2 = ax2.bar(objects2, momenta2, color=colors2, alpha=0.8, edgecolor='black', linewidth=2, zorder=3)
        
        # Add value labels on bars
        for bar, value in zip(bars2, momenta2):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{value:.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold')
        
        # Add equation text
        ax2.text(0.5, max(momenta2)*0.5, f'p_total = p₁ + p₂\n{p_total:.2f} = {p1:.2f} + {p2:.2f}',
                transform=ax2.transData, ha='center', fontsize=10, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.7', facecolor='lightyellow', alpha=0.7))
        
        ax2.set_ylabel('Momentum (kg·m/s)', fontsize=11, fontweight='bold')
        ax2.set_title('Momentum Conservation', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3, axis='y', linestyle='--')
        ax2.set_ylim(0, max(momenta2) * 1.3)
        
        fig.tight_layout()
