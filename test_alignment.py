#!/usr/bin/env python3
"""
test_alignment.py

File Purpose: Test script to verify llamaline's alignment improvements
Primary Functions/Classes: Tests startup menu and splash screen alignment
Inputs and Outputs (I/O): Visual verification of UI alignment
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'llamaline'))

from llamaline import show_startup_menu, console

def test_alignment():
    """Test the alignment of startup components"""
    console.print("=== Testing Llamaline Alignment ===\n")
    
    # Test startup menu
    show_startup_menu('gemma3:4b', 'http://localhost:11434')
    
    console.print("\n=== Alignment Test Complete ===")

if __name__ == "__main__":
    test_alignment() 