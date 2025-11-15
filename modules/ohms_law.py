"""
Ohm's Law Module
V = IR calculations with visualization
"""

import customtkinter as ctk
from tkinter import messagebox
import numpy as np
from utils.validators import safe_float
from utils.plotter import create_plot

class OhmsLawModule:
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
            text="Ohm's Law Calculator",
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
            text="Enter any 2 values to calculate the 3rd",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(pady=(0, 15), padx=20)
        
        # Input fields
        fields = [
            ("Voltage (V) [Volts]:", "V"),
            ("Current (I) [Amperes]:", "I"),
            ("Resistance (R) [Ohms]:", "R")
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
            text="Ohm's Law:\nV = I × R\n\n"
                 "Where:\n"
                 "V = Voltage (Volts)\n"
                 "I = Current (Amperes)\n"
                 "R = Resistance (Ohms)",
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="gray"
        )
        info.pack(pady=10, padx=20)
        
    def calculate(self):
        """Perform Ohm's Law calculations"""
        try:
            # Get inputs
            v_str = self.entries['V'].get().strip()
            i_str = self.entries['I'].get().strip()
            r_str = self.entries['R'].get().strip()
            
            # Count filled values
            filled = sum([bool(v_str), bool(i_str), bool(r_str)])
            
            if filled != 2:
                messagebox.showerror("Error", "Please enter exactly 2 values!")
                return
            
            steps = ["Given:"]
            
            # Calculate missing value
            if not v_str:  # Calculate V
                I = safe_float(i_str, "Current")
                R = safe_float(r_str, "Resistance")
                if I <= 0 or R <= 0:
                    messagebox.showerror("Error", "Current and Resistance must be positive!")
                    return
                V = I * R
                steps.append(f"  I = {I} A")
                steps.append(f"  R = {R} Ω")
                steps.append("")
                steps.append("Calculating Voltage:")
                steps.append("  V = I × R")
                steps.append(f"  V = {I} × {R}")
                steps.append(f"  V = {V:.3f} Volts")
                result_var = "V"
                result_val = V
                
            elif not i_str:  # Calculate I
                V = safe_float(v_str, "Voltage")
                R = safe_float(r_str, "Resistance")
                if V < 0 or R <= 0:
                    messagebox.showerror("Error", "Voltage must be non-negative and Resistance positive!")
                    return
                I = V / R
                steps.append(f"  V = {V} V")
                steps.append(f"  R = {R} Ω")
                steps.append("")
                steps.append("Calculating Current:")
                steps.append("  I = V / R")
                steps.append(f"  I = {V} / {R}")
                steps.append(f"  I = {I:.3f} Amperes")
                result_var = "I"
                result_val = I
                R_for_plot = R
                
            else:  # Calculate R
                V = safe_float(v_str, "Voltage")
                I = safe_float(i_str, "Current")
                if V < 0 or I <= 0:
                    messagebox.showerror("Error", "Voltage must be non-negative and Current positive!")
                    return
                R = V / I
                steps.append(f"  V = {V} V")
                steps.append(f"  I = {I} A")
                steps.append("")
                steps.append("Calculating Resistance:")
                steps.append("  R = V / I")
                steps.append(f"  R = {V} / {I}")
                steps.append(f"  R = {R:.3f} Ohms")
                result_var = "R"
                result_val = R
            
            # Get all values for plotting
            if not v_str:
                V_final, I_final, R_final = V, I, R
            elif not i_str:
                V_final, I_final, R_final = V, I, R
            else:
                V_final, I_final, R_final = V, I, R
            
            # Display results
            self.display_results(steps, V_final, I_final, R_final)
            
            # Save to history
            self.save_callback(
                "Ohm's Law",
                {"V": V_final, "I": I_final, "R": R_final},
                {result_var: result_val}
            )
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Calculation error: {str(e)}")
    
    def display_results(self, steps, V, I, R):
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
        
        solution_text = ctk.CTkTextbox(steps_frame, height=140, font=ctk.CTkFont(family="Courier", size=10))
        solution_text.pack(pady=(0, 10), padx=15, fill="both", expand=True)
        solution_text.insert("1.0", "\n".join(steps))
        solution_text.configure(state="disabled")
        
        # Create plot
        plot_frame = ctk.CTkFrame(self.output_frame)
        plot_frame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))
        self.output_frame.grid_rowconfigure(1, weight=1)
        
        # Generate V-I characteristic
        current_array = np.linspace(0, max(I * 2, 0.1), 100)
        voltage_array = R * current_array
        
        fig = create_plot(plot_frame, figsize=(8, 6))
        ax = fig.add_subplot(1, 1, 1)
        
        # Plot characteristic curve
        ax.plot(current_array, voltage_array, 'b-', linewidth=2.5, label=f'V = {R:.2f}Ω × I', zorder=3)
        
        # Plot operating point
        ax.scatter([I], [V], color='red', s=150, zorder=5, edgecolors='darkred', linewidth=2.5, label=f'Operating Point')
        
        # Add reference lines
        ax.axhline(y=V, color='red', linestyle='--', alpha=0.4, linewidth=1.5)
        ax.axvline(x=I, color='red', linestyle='--', alpha=0.4, linewidth=1.5)
        
        # Fill area under curve to operating point
        fill_current = np.linspace(0, I, 50)
        fill_voltage = R * fill_current
        ax.fill_between(fill_current, fill_voltage, alpha=0.15, color='blue', zorder=1)
        
        # Add annotation with detailed info
        textstr = f'I = {I:.3f} A\nV = {V:.3f} V\nR = {R:.3f} Ω\nP = {V*I:.3f} W'
        ax.annotate(textstr, 
                   xy=(I, V), xytext=(I+max(I*0.3, 0.05), V+abs(V)*0.2),
                   arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
                   fontsize=10, color='red', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.3))
        
        ax.set_xlabel('Current (A)', fontsize=11, fontweight='bold')
        ax.set_ylabel('Voltage (V)', fontsize=11, fontweight='bold')
        ax.set_title(f'V-I Characteristic Curve (Resistance = {R:.2f}Ω)', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.4, linestyle='--')
        ax.legend(fontsize=10, loc='best')
        
        # Add minor gridlines
        ax.minorticks_on()
        ax.grid(True, which='minor', alpha=0.2, linestyle=':')
        
        fig.tight_layout()
