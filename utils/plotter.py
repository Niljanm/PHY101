"""
Plotting Utilities
Helper functions for creating and embedding matplotlib plots in CustomTkinter
"""

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Set matplotlib style
plt.style.use('seaborn-v0_8-darkgrid')


def create_plot(parent_frame, figsize=(8, 6), dpi=100):
    """
    Create a matplotlib figure and embed it in a CustomTkinter frame
    
    Args:
        parent_frame: The CTkFrame to embed the plot in
        figsize: Tuple of (width, height) in inches
        dpi: Dots per inch for the figure
        
    Returns:
        Figure: The created matplotlib figure
    """
    # Clear any existing widgets in the frame
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Create figure
    fig = Figure(figsize=figsize, dpi=dpi, facecolor='#2b2b2b')
    
    # Create canvas
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    
    # Pack canvas
    canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
    
    return fig


def clear_plot(parent_frame):
    """
    Clear all plots from a frame
    
    Args:
        parent_frame: The CTkFrame containing plots
    """
    for widget in parent_frame.winfo_children():
        widget.destroy()


def save_plot(fig, filename="plot.png", dpi=300):
    """
    Save a matplotlib figure to file
    
    Args:
        fig: The matplotlib figure to save
        filename: Output filename
        dpi: Resolution for the saved image
    """
    try:
        fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor='white')
        print(f"Plot saved to {filename}")
    except Exception as e:
        print(f"Error saving plot: {e}")


def configure_dark_theme(ax):
    """
    Configure a matplotlib axes for dark theme
    
    Args:
        ax: Matplotlib axes object
    """
    ax.set_facecolor('#2b2b2b')
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')


def configure_light_theme(ax):
    """
    Configure a matplotlib axes for light theme
    
    Args:
        ax: Matplotlib axes object
    """
    ax.set_facecolor('white')
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    ax.title.set_color('black')
    ax.tick_params(axis='x', colors='black')
    ax.tick_params(axis='y', colors='black')


def create_subplot_grid(parent_frame, rows, cols, figsize=(10, 8)):
    """
    Create a grid of subplots
    
    Args:
        parent_frame: The CTkFrame to embed the plots in
        rows: Number of rows in the grid
        cols: Number of columns in the grid
        figsize: Tuple of (width, height) in inches
        
    Returns:
        tuple: (Figure, array of Axes objects)
    """
    # Clear any existing widgets
    for widget in parent_frame.winfo_children():
        widget.destroy()
    
    # Create figure with subplots
    fig, axes = plt.subplots(rows, cols, figsize=figsize, facecolor='#2b2b2b')
    
    # Create canvas
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True, padx=5, pady=5)
    
    return fig, axes


def add_watermark(ax, text="Physics Calculator"):
    """
    Add a watermark to a plot
    
    Args:
        ax: Matplotlib axes object
        text: Watermark text
    """
    ax.text(0.99, 0.01, text, 
            transform=ax.transAxes,
            fontsize=8, color='gray',
            alpha=0.5, ha='right', va='bottom',
            style='italic')


def export_figure_png(fig, filename="graph.png", dpi=300):
    """
    Export figure as PNG image
    
    Args:
        fig: Matplotlib figure object
        filename: Output PNG filename
        dpi: Resolution in dots per inch
        
    Returns:
        str: Filename if successful, None otherwise
    """
    try:
        fig.savefig(filename, dpi=dpi, bbox_inches='tight', facecolor='#2b2b2b')
        return filename
    except Exception as e:
        print(f"Error exporting PNG: {e}")
        return None


def export_figure_pdf(fig, filename="graph.pdf"):
    """
    Export figure as PDF
    
    Args:
        fig: Matplotlib figure object
        filename: Output PDF filename
        
    Returns:
        str: Filename if successful, None otherwise
    """
    try:
        fig.savefig(filename, format='pdf', bbox_inches='tight', facecolor='#2b2b2b')
        return filename
    except Exception as e:
        print(f"Error exporting PDF: {e}")
        return None
