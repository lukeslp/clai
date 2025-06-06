# 🦙 llamaline v1.0.0 - First Stable Release

**Transform your everyday tasks into simple English commands!**

llamaline is a natural-language to shell/Python CLI assistant that bridges the gap between natural language and code execution, making command-line operations accessible to everyone.

## ✨ What's New in v1.0.0

### 🚀 Core Features
- **Natural Language Processing**: Convert English prompts to executable bash/Python code using local Ollama models
- **Interactive CLI**: Rich-styled command-line interface with colorized output and confirmation prompts
- **Cheat Sheet Library**: Predefined shortcuts for common tasks (disk usage, file listing, process monitoring, etc.)
- **Safety Features**: Command confirmation, unsafe operation blocking, and dry-run previews
- **Flexible Configuration**: Environment variable and CLI flag overrides for Ollama endpoint and model selection
- **Single-Shot Execution**: Run commands directly from CLI arguments (`llamaline "show disk usage"`)
- **Model Switching**: Change Ollama models on-the-fly during interactive sessions

### 🛠 Technical Capabilities
- **Python Execution**: Execute Python snippets in temporary files with pretty-printed JSON output
- **Bash Execution**: Run shell commands with safety checks to prevent destructive operations
- **Rich Output**: Formatted console output with syntax highlighting and panels
- **Error Handling**: Comprehensive error reporting and graceful failure handling

### 🎯 Accessibility Features
- Keyboard-only navigation (no mouse required)
- Colorized output with plain text fallbacks
- Clear command structure and help system
- Screen reader compatible interface

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/lukeslp/llamaline.git
cd llamaline
pip install .
```

### Usage Examples
```bash
# Single commands
llamaline "Show me disk usage"
llamaline "List all Python files"
llamaline "What processes are using the most memory?"

# Interactive mode
llamaline
> memory usage
> running processes
> say hello
> list files
```

### Built-in Cheat Sheets
- `disk usage` → `df -h`
- `list files` → `ls -al`
- `memory usage` → `vm_stat`
- `running processes` → `ps aux`
- `network ports` → `lsof -i -P -n | grep LISTEN`
- `current directory` → `pwd`
- `say hello` → `print('Hello, world!')`

## 📋 Requirements
- **Python 3.7+**
- **Local Ollama server** with at least one model installed
  - Install Ollama: [https://ollama.com](https://ollama.com)
  - Recommended: `ollama pull gemma3:4b`
  - Or any compatible model you prefer

## ⚙️ Configuration

### Environment Variables
```bash
export OLLAMA_ENDPOINT="http://localhost:11434"  # Default
export OLLAMA_MODEL="gemma3:4b"                  # Default
```

### Command Line Options
```bash
llamaline -e http://localhost:11434 -m llama2 "your command"
llamaline --help  # Show all options
```

## 🔒 Safety Features
- **Command confirmation** before execution
- **Unsafe operation blocking** (prevents `sudo`, `rm -rf`, etc.)
- **Temporary file execution** for Python code
- **No persistent state** between commands
- **Input validation** and error handling

## 🎯 Example Session

```
llamaline
Model: gemma3:4b   Endpoint: http://localhost:11434
Commands: help cheats quit model <n>

Enter your task (or 'quit' to exit):
> show me disk usage

[Preview] bash code:
df -h

Execute this? [Y/n]: y
$ df -h

=== Bash Output ===
Filesystem      Size   Used  Avail Capacity
/dev/disk1s1   932Gi  234Gi  697Gi    26%
...

Enter your task (or 'quit' to exit):
> create a hello world python script

[Preview] python code:
print('Hello, world!')

Execute this? [Y/n]: y
```python
print('Hello, world!')
```

=== Python Output ===
Hello, world!
```

## 🛠 Development

### Project Structure
```
llamaline/
├── llamaline/
│   ├── __init__.py
│   └── llamaline.py      # Main CLI module
├── setup.py              # Package configuration
├── requirements.txt      # Dependencies
├── PROJECT_PLAN.md       # Roadmap and architecture
├── CHANGELOG.md          # Version history
└── README.md            # Documentation
```

### Dependencies
- `colorama` - ANSI color support
- `rich` - Rich text and beautiful formatting
- `requests` - HTTP client for Ollama API

## 🌟 Community & Support

- 🐛 [Report Issues](https://github.com/lukeslp/llamaline/issues)
- 🛠️ [Source Code](https://github.com/lukeslp/llamaline)
- 📧 [Email](mailto:luke@lukesteuber.com)
- 🐦 [Bluesky](https://bsky.app/profile/lukesteuber.com)
- 💼 [LinkedIn](https://www.linkedin.com/in/lukesteuber/)
- ✉️ [Newsletter](https://lukesteuber.substack.com/)
- ☕ [Support Development](https://usefulai.lemonsqueezy.com/buy/bf6ce1bd-85f5-4a09-ba10-191a670f74af)

## 📄 License

Licensed under the **MIT License** by Luke Steuber. See [LICENSE](LICENSE) for details.

---

**Made with ❤️ for the accessibility community**

*This release represents the first stable version of llamaline, providing a solid foundation for natural-language command-line interaction with comprehensive safety features and accessibility support.* 