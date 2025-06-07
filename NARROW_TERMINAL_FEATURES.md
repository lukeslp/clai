"""
NARROW_TERMINAL_FEATURES.md

File Purpose: Comprehensive documentation for llamaline's narrow terminal support and rich styling
Primary Sections: Features overview, responsive design, alignment fixes, usage examples
Inputs and Outputs (I/O): User guide for optimal CLI experience across all terminal sizes
"""

# 📱 Llamaline: Narrow Terminal & Rich Styling Features

## 🎯 Overview

Llamaline has been completely redesigned to work beautifully on terminals of all sizes, from mobile SSH clients with 30 columns to full-screen developer workstations. The CLI automatically adapts its interface based on your terminal width, ensuring an optimal experience regardless of your environment.

## ✨ Key Improvements Made

### 1. **Perfect Alignment**
- ✅ **Fixed**: ASCII art and info panel are now perfectly centered and aligned
- ✅ **Responsive Width**: Panel width automatically matches content width
- ✅ **Centered Layout**: Both splash screen and startup menu use `Align.center`
- ✅ **Clean Markup**: Proper handling of Rich markup in width calculations

### 2. **Comprehensive Rich Styling**
- 🎨 **Custom Theme**: Semantic color scheme (cyan=info, red=error, green=success)
- 🌈 **Syntax Highlighting**: Python and Bash code with Monokai theme
- ⏳ **Progress Indicators**: Animated spinners for all operations
- 📦 **Styled Panels**: Consistent borders and titles throughout
- 🎭 **Emoji Support**: Visual cues with text fallbacks

### 3. **Narrow Terminal Optimization**
- 📱 **Ultra-Narrow (< 40 cols)**: Minimal UI, shortened prompts
- 📱 **Narrow (40-50 cols)**: Compact mode, essential info only
- 💻 **Standard (50-60 cols)**: Most features, no line numbers
- 🖥️ **Wide (> 60 cols)**: Full feature set with splash screen

## 🔧 Technical Implementation

### Responsive Design Functions

```python
def get_terminal_width() -> int:
    """Get current terminal width for responsive design"""
    return console.width

def create_responsive_panel(content: str, title: str = "", 
                          border_style: str = "cyan") -> Panel:
    """Create panels that adapt to terminal width"""
    terminal_width = get_terminal_width()
    panel_width = min(int(terminal_width * 0.9), terminal_width - 2)
    wrapped_content = wrap_text(content, panel_width - 4)
    return Panel(wrapped_content, title=title, border_style=border_style)
```

### Alignment System

```python
def show_startup_menu(model: str, endpoint: str):
    """Display startup menu with perfect alignment"""
    # Calculate optimal panel width based on content
    content_lines = content.split('\n')
    clean_lines = [re.sub(r'\[.*?\]', '', line) for line in content_lines]
    max_content_width = max(len(line) for line in clean_lines)
    panel_width = min(max_content_width + 8, terminal_width - 2)
    
    # Center everything
    panel = Panel(content, width=panel_width, expand=False)
    console.print(Align.center(panel))
```

## 📊 Terminal Width Behaviors

| Width Range | Mode | Features |
|-------------|------|----------|
| < 40 chars | Ultra-Compact | Minimal UI, "Task:" prompt, no splash |
| 40-50 chars | Compact | Essential info, truncated outputs (20 lines) |
| 50-60 chars | Standard | Most features, simplified cheat sheet |
| > 60 chars | Full | Splash screen, line numbers, full info |

## 🎨 Rich Styling Features

### Color Theme
```python
custom_theme = Theme({
    "info": "cyan",           # Information messages
    "warning": "yellow",      # Warnings and cancellations  
    "error": "bold red",      # Error messages
    "success": "bold green",  # Success confirmations
    "prompt": "bold magenta", # User input prompts
    "code": "bold blue",      # Code previews
    "dim": "dim white",       # Secondary information
})
```

### Interactive Elements

1. **Progress Spinners**
   ```
   ⠋ Analyzing prompt and generating code...
   ⠙ Running python code...
   ```

2. **Syntax Highlighting**
   - Python code with line numbers (wide terminals)
   - Bash commands with appropriate coloring
   - Automatic word wrapping

3. **Styled Panels**
   ```
   ╭─ 💻 Python Code Preview ─╮
   │ print("Hello, world!")   │
   ╰──────────────────────────╯
   ```

4. **Rich Prompts**
   - Styled input with default values
   - Y/N confirmations with Rich.Confirm
   - Responsive prompt text

## 📱 Mobile & SSH Optimization

### For Mobile SSH Clients
- Automatic detection of narrow terminals
- Simplified UI that fits small screens
- All functionality preserved
- Touch-friendly (no mouse required)

### For tmux/screen Users
- Panels automatically resize when splitting panes
- Use `clear` command after resizing for best results
- All animations are tmux-friendly

## 🛠️ New Commands Added

| Command | Description | Responsive |
|---------|-------------|------------|
| `history` | Show last 10 commands | ✅ Truncates on narrow |
| `clear` | Clear screen and reset display | ✅ Responsive startup |
| `help` | Show available commands | ✅ Table vs list layout |
| `cheats` | Display shortcut table | ✅ Adaptive columns |

## 🎯 Usage Examples

### Wide Terminal (80+ columns)
```
    ╦  ╦  ╔═╗╔╦╗╔═╗╦  ╦╔╗╔╔═╗
    ║  ║  ╠═╣║║║╠═╣║  ║║║║║╣ 
    ╩═╝╩═╝╩ ╩╩ ╩╩ ╩╩═╝╩╝╚╝╚═╝
    Natural Language → Code

╭─────────────── 🚀 Llamaline CLI ───────────────╮
│ Model: gemma3:4b   Endpoint: http://localhost  │
│ Commands: help • cheats • model • quit         │
╰─────────────────────────────────────────────────╯

Enter your task (or 'quit' to exit): disk usage

⠋ Analyzing prompt and generating code...

╭─ 💻 Bash Code Preview ──────────────────────────╮
│ 1 │ df -h                                      │
╰──────────────────────────────────────────────────╯

Execute this code? [y/n] (y): y

⠙ Running bash code...

╭─ ✅ Bash Output ────────────────────────────────╮
│ Filesystem      Size  Used Avail Use% Mounted  │
│ /dev/sda1        50G   30G   20G  60% /        │
╰──────────────────────────────────────────────────╯
```

### Narrow Terminal (40 columns)
```
╭─ Llamaline ──────────────────╮
│ Model: gemma3:4b             │
│ Type help for commands       │
╰──────────────────────────────╯

Task: disk usage

⠋ Analyzing...

╭─ Bash ───────────────────────╮
│ df -h                        │
╰──────────────────────────────╯

Execute? [y/n] (y): y

⠙ Running...

╭─ Output ─────────────────────╮
│ Filesystem  Size  Used Avail │
│ /dev/sda1   50G   30G   20G  │
╰──────────────────────────────╯
```

## 🔍 Testing & Validation

### Test Script
```bash
# Test different terminal widths
python test_narrow_terminal.py

# Test alignment
python test_alignment.py

# Interactive testing
python -m llamaline.llamaline
```

### Manual Testing
1. Resize terminal to different widths
2. Use `clear` command to see responsive startup
3. Try all commands (`help`, `cheats`, `history`)
4. Test with long outputs and code snippets

## 🚀 Performance Optimizations

- **Lazy Loading**: Rich components loaded only when needed
- **Efficient Rendering**: Minimal redraws and smart caching
- **Memory Management**: Temporary files cleaned up automatically
- **Responsive Calculations**: Width detection cached per operation

## 🎨 Accessibility Features

- **Screen Reader Compatible**: All visual elements have text alternatives
- **High Contrast**: Clear color distinctions for visibility
- **Keyboard Only**: No mouse interaction required
- **Semantic Markup**: Proper use of Rich's semantic styling

## 📝 Summary

The llamaline CLI now provides a world-class experience across all terminal sizes:

✅ **Perfect Alignment**: Splash screen and panels are properly centered  
✅ **Responsive Design**: Adapts to any terminal width (30-200+ columns)  
✅ **Rich Styling**: Beautiful syntax highlighting and progress indicators  
✅ **Mobile Friendly**: Optimized for SSH clients and narrow terminals  
✅ **Full Functionality**: No features lost on narrow terminals  
✅ **Accessibility**: Screen reader compatible with semantic styling  

Whether you're using llamaline on a mobile device, in a tmux pane, or on a full desktop terminal, you'll get a beautiful, functional experience that adapts perfectly to your environment.

---
*For more information, see the main [README.md](README.md) and [PROJECT_PLAN.md](PROJECT_PLAN.md)* 