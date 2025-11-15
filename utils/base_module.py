"""
Module Base Class with Common Features
Provides reset, copy, export, presets, and tooltips functionality
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
from utils.tooltips import create_tooltip
from utils.presets import get_presets
import pyperclip
from utils.plotter import export_figure_png, export_figure_pdf


class BasePhysicsModule:
    """Base class for physics modules with common features"""
    
    def __init__(self, parent, save_callback, module_name, preset_key):
        self.parent = parent
        self.save_callback = save_callback
        self.module_name = module_name
        self.preset_key = preset_key
        self.entries = {}
        self.current_figure = None
        self.last_results = None
    
    def add_tooltip(self, widget, tooltip_text):
        """Add tooltip to widget"""
        create_tooltip(widget, tooltip_text)
    
    def create_control_buttons(self, button_frame):
        """Create common control buttons (Reset, Copy, Export)"""
        ctk.CTkButton(
            button_frame,
            text="Reset",
            command=self.reset_inputs,
            fg_color="#505050",
            hover_color="#404040",
            height=35,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Copy Results",
            command=self.copy_results,
            fg_color="#505050",
            hover_color="#404040",
            height=35,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            button_frame,
            text="Export Graph",
            command=self.export_graph,
            fg_color="#505050",
            hover_color="#404040",
            height=35,
            font=ctk.CTkFont(size=11)
        ).pack(side="left", padx=5)
    
    def create_presets_dropdown(self, parent_frame):
        """Create preset examples dropdown"""
        preset_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        preset_frame.pack(pady=10, padx=20, fill="x")
        
        ctk.CTkLabel(
            preset_frame,
            text="Examples:",
            font=ctk.CTkFont(size=11, weight="bold")
        ).pack(side="left", padx=(0, 10))
        
        presets = get_presets(self.preset_key)
        preset_names = [p["name"] for p in presets] if presets else []
        
        if preset_names:
            self.preset_var = ctk.StringVar(value="Load Example...")
            preset_combo = ctk.CTkComboBox(
                preset_frame,
                values=preset_names,
                variable=self.preset_var,
                command=self.load_preset,
                state="readonly"
            )
            preset_combo.pack(side="left", fill="x", expand=True)
    
    def load_preset(self, preset_name):
        """Load a preset into input fields"""
        if preset_name == "Load Example...":
            return
        
        presets = get_presets(self.preset_key)
        for preset in presets:
            if preset["name"] == preset_name:
                values = preset["values"]
                for key, value in values.items():
                    if key in self.entries:
                        self.entries[key].delete(0, "end")
                        self.entries[key].insert(0, value)
                break
    
    def reset_inputs(self):
        """Clear all input fields"""
        for entry in self.entries.values():
            entry.delete(0, "end")
        
        if hasattr(self, 'output_frame'):
            for widget in self.output_frame.winfo_children():
                widget.destroy()
    
    def copy_results(self):
        """Copy last results to clipboard"""
        if not self.last_results:
            messagebox.showwarning("Copy", "No results to copy. Please calculate first.")
            return
        
        try:
            text = f"Module: {self.module_name}\n"
            text += f"Results:\n"
            for key, value in self.last_results.items():
                text += f"  {key}: {value}\n"
            pyperclip.copy(text)
            messagebox.showinfo("Copy", "Results copied to clipboard!")
        except Exception as e:
            messagebox.showerror("Error", f"Could not copy to clipboard: {str(e)}")
    
    def export_graph(self):
        """Export current graph as PNG or PDF"""
        if not self.current_figure:
            messagebox.showwarning("Export", "No graph to export. Please calculate first.")
            return
        
        # Ask for file format
        format_choice = messagebox.askyesno("Export Format", "Use PDF format?\n(Yes=PDF, No=PNG)")
        
        if format_choice is None:
            return
        
        file_ext = "pdf" if format_choice else "png"
        file_types = [("PDF files", "*.pdf"), ("All files", "*.*")] if format_choice else [("PNG files", "*.png"), ("All files", "*.*")]
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{file_ext}",
            filetypes=file_types
        )
        
        if file_path:
            if format_choice:
                result = export_figure_pdf(self.current_figure, file_path)
            else:
                result = export_figure_png(self.current_figure, file_path)
            
            if result:
                messagebox.showinfo("Success", f"Graph exported to:\n{result}")
            else:
                messagebox.showerror("Error", "Failed to export graph")
    
    def store_figure(self, fig):
        """Store the current figure for export"""
        self.current_figure = fig
    
    def store_results(self, results):
        """Store the last calculation results"""
        self.last_results = results
