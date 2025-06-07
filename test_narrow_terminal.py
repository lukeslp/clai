#!/usr/bin/env python3
"""
test_narrow_terminal.py

File Purpose: Test script to demonstrate llamaline's narrow terminal support
Primary Functions/Classes: Simulates different terminal widths and shows adaptive UI
Inputs and Outputs (I/O): Terminal width simulation and visual output demonstration
"""

import os
import sys
from rich.console import Console

# Import our terminal utilities from llamaline
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'llamaline'))
from llamaline import (
    get_terminal_width, create_responsive_panel, 
    show_cheat_sheet, show_help, display_code_preview
)

def demonstrate_terminal_widths():
    """Show how llamaline adapts to different terminal widths"""
    
    print("=== Llamaline Narrow Terminal Support Demo ===\n")
    
    # Test different terminal widths
    widths = [30, 40, 50, 60, 80, 120]
    
    for width in widths:
        # Create console with specific width
        console = Console(width=width)
        print(f"\n{'='*width}")
        print(f"Terminal Width: {width} columns")
        print(f"{'='*width}\n")
        
        # Show how panels adapt
        panel = create_responsive_panel(
            "This is a test panel that demonstrates text wrapping and responsive design. "
            "The panel automatically adjusts its width and wraps content to fit the terminal.",
            title="📱 Responsive Panel",
            border_style="cyan"
        )
        console.print(panel)
        
        # Show code preview adaptation
        if width >= 40:
            print("\nCode Preview:")
            sample_code = """def hello_world():
    print("Hello from llamaline!")
    return True"""
            display_code_preview("python", sample_code)
        
        input("\nPress Enter to continue...")
        os.system('clear' if os.name != 'nt' else 'cls')

if __name__ == "__main__":
    try:
        demonstrate_terminal_widths()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted.")
    except Exception as e:
        print(f"\nNote: This demo requires the llamaline package to be installed.")
        print(f"Error: {e}")
        print("\nShowing basic width demonstration instead:\n")
        
        # Basic demo without llamaline imports
        widths = [30, 40, 50, 60, 80]
        for width in widths:
            print(f"{'='*min(width, 80)}")
            print(f"Width: {width} - ", end="")
            if width < 40:
                print("Ultra-narrow mode")
            elif width < 50:
                print("Narrow mode")
            elif width < 60:
                print("Standard mode")
            else:
                print("Wide mode")
            print(f"{'='*min(width, 80)}\n") 