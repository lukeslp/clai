"""
NARROW_TERMINAL_GUIDE.md

File Purpose: Documentation for llamaline's narrow terminal support and rich styling features
Primary Sections: Terminal width behaviors, responsive design, rich features, usage tips
Inputs and Outputs (I/O): User guide for optimal CLI experience across different terminal sizes
"""

# 📱 Narrow Terminal & Rich Styling Guide

This guide covers llamaline's comprehensive support for narrow terminals and rich interactive features.

## 🎯 Overview

Llamaline is designed to work beautifully on terminals of all sizes, from mobile SSH clients with 40 columns to full-screen developer workstations. The CLI automatically adapts its interface based on your terminal width, ensuring an optimal experience regardless of your environment.

## 📏 Terminal Width Behaviors

### Ultra-Narrow (< 40 columns)
- Minimal UI with essential information only
- Shortened prompts ("Task:" instead of full prompt)
- Simplified output panels
- No splash screen
- Compact error messages
- Single-column help display

### Narrow (40-50 columns)  
- Compact mode with core features
- Abbreviated panel titles
- Truncated long outputs (20 lines max)
- Simplified cheat sheet table
- Basic progress indicators

### Standard (50-60 columns)
- Most features visible
- Standard panel titles with some emoji
- Code preview without line numbers
- Two-column cheat sheet (command + description)
- Full progress indicators

### Wide (> 60 columns)
- Full feature set enabled
- Splash screen on startup
- Code preview with syntax highlighting and line numbers
- Multi-column cheat sheet with all details
- Extended panel titles with emoji
- Model and endpoint info displayed together

## 🎨 Rich Styling Features

### Color Theme
Llamaline uses a consistent color theme throughout:
- **Cyan**: Information and headers
- **Yellow**: Warnings and model info
- **Red**: Errors and cancellations
- **Green**: Success messages and output
- **Magenta**: User prompts
- **Blue**: Code preview and history
- **Dim white**: Secondary information

### Progress Indicators
All long-running operations show animated progress:
```
⠋ Analyzing prompt and generating code...
⠙ Running bash code...
```

### Syntax Highlighting
Code is displayed with full syntax highlighting:
- Python code with Monokai theme
- Bash commands with appropriate coloring
- Line numbers on wide terminals
- Automatic word wrapping

### Interactive Panels
All output is wrapped in styled panels:
```
╭─ 💻 Python Code Preview ─────────────╮
│ print("Hello, world!")               │
╰──────────────────────────────────────╯
```

## 🛠️ Responsive Design Features

### Text Wrapping
All text content automatically wraps to fit your terminal:
- Long commands are wrapped with proper indentation
- Output is intelligently truncated with line counts
- Panel content adjusts to available width

### Dynamic Tables
The cheat sheet command (`cheats`) adapts its display:
- **Wide**: Command | Type | Code | Description
- **Narrow**: Command | Description only

### Adaptive Prompts
Input prompts adjust based on width:
- **Wide**: "Enter your task (or 'quit' to exit):"
- **Narrow**: "Task:"

### Smart Truncation
Long outputs are truncated based on terminal width:
- Narrow terminals: 20 lines max
- Wide terminals: 50 lines max
- Shows count of hidden lines

## 💡 Usage Tips

### For Mobile/SSH Users
1. llamaline works great on mobile SSH clients
2. Use `clear` command to reset display if needed
3. History command shows last 10 commands
4. All features accessible via keyboard

### For tmux/screen Users
1. Panels automatically resize when splitting panes
2. Use `clear` after resizing for best results
3. All animations are tmux-friendly

### For Accessibility
1. All emoji have text alternatives
2. Color is never the only indicator
3. Screen readers work with all output
4. High contrast themes supported

## 🎯 Best Practices

### Terminal Setup
- Set terminal to at least 40 columns wide
- UTF-8 encoding recommended for best display
- 256-color terminal for syntax highlighting

### Using Commands
- Type `help` to see available commands
- Use `history` to recall previous commands
- `clear` resets the display
- `cheats` shows available shortcuts

### Customization
Environment variables for customization:
```bash
# Change model
export OLLAMA_MODEL="llama2"

# Change endpoint  
export OLLAMA_ENDPOINT="http://localhost:11434"
```

## 🔧 Troubleshooting

### Display Issues
- **Garbled output**: Ensure UTF-8 encoding
- **Missing colors**: Check terminal supports 256 colors
- **Broken panels**: Try `clear` command
- **Text overflow**: Terminal might be too narrow

### Performance
- Progress indicators show operation status
- Narrow terminals get faster, simpler displays
- Use Ctrl+C to interrupt long operations

## 📝 Examples

### Narrow Terminal Session (40 cols)
```
╭─ Llamaline ──────────────────╮
│ Model: gemma3:4b             │
│ Type help for commands       │
╰──────────────────────────────╯

[prompt]Task:[/prompt] disk usage

⠋ Analyzing prompt...

╭─ Bash ───────────────────────╮
│ df -h                        │
╰──────────────────────────────╯

[prompt]Execute?[/prompt] Y

✅ Output
Filesystem  Size  Used  Avail
/dev/sda1   50G   30G   20G
```

### Wide Terminal Session (80+ cols)
```
    ╦  ╦  ╔═╗╔╦╗╔═╗╦  ╦╔╗╔╔═╗
    ║  ║  ╠═╣║║║╠═╣║  ║║║║║╣ 
    ╩═╝╩═╝╩ ╩╩ ╩╩ ╩╩═╝╩╝╚╝╚═╝
    Natural Language → Code

╭─ 🚀 Llamaline CLI ─────────────────────────────────╮
│ Model: gemma3:4b   Endpoint: http://localhost:11434│
│ Commands: help • cheats • model • quit             │
╰────────────────────────────────────────────────────╯

[prompt]Enter your task (or 'quit' to exit):[/prompt] show system info

⠋ Analyzing prompt and generating code...

╭─ 💻 Python Code Preview ────────────────────────────╮
│ 1 │ import platform                                │
│ 2 │ import os                                       │
│ 3 │ print(f"System: {platform.system()}")          │
│ 4 │ print(f"Node: {platform.node()}")              │
│ 5 │ print(f"Python: {platform.python_version()}")  │
╰─────────────────────────────────────────────────────╯

[prompt]Execute this code?[/prompt] Y

⠙ Running python code...

╭─ ✅ Python Output ──────────────────────────────────╮
│ System: Linux                                       │
│ Node: workstation                                   │  
│ Python: 3.11.5                                      │
╰─────────────────────────────────────────────────────╯
```

## 🌟 Summary

Llamaline's narrow terminal support and rich styling ensure a great experience regardless of your terminal size. The responsive design means you can use llamaline anywhere - from a mobile SSH session to a full desktop terminal - with all features adapting automatically to provide the best possible interface.

---
*For more information, see the main [README.md](README.md)* 