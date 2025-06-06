---
**llamaline v1.0.0**  
MIT License  
Author: Luke Steuber  
Web: [actuallyusefulai.com](https://actuallyusefulai.com), [lukesteuber.com](https://lukesteuber.com)
---

# 🦙 llamaline

**A natural-language to shell/Python CLI assistant using local Ollama models.**

Transform your everyday tasks into simple English commands! llamaline bridges the gap between natural language and code execution, making command-line operations accessible to everyone.

## ✨ Features

- 🗣️ **Natural Language Processing**: Type commands in plain English
- 🛡️ **Safety First**: Confirmation prompts and unsafe operation blocking  
- 🎨 **Rich Interface**: Colorized output with syntax highlighting
- ⚡ **Quick Commands**: Built-in cheat sheets for common tasks
- 🔄 **Model Flexibility**: Switch between Ollama models on-the-fly
- 🎯 **Accessibility**: Full keyboard navigation, screen reader compatible
- 🔧 **Developer Friendly**: Easy installation and configuration

## Installation

```bash
pip install .
```

Or, for development:

```bash
pip install -e .
```

## 🚀 Quick Start

### Single Command Execution
```bash
llamaline "Show me disk usage"
llamaline "List all Python files in this directory"
llamaline "What's my current memory usage?"
```

### Interactive Mode
```bash
llamaline
```

Then type natural language commands:
- `disk usage` → `df -h`
- `running processes` → `ps aux`
- `say hello` → `print('Hello, world!')`
- `list files` → `ls -al`

### Built-in Commands
- `help` - Show available commands
- `cheats` - List all cheat sheet shortcuts
- `model` - Show current Ollama model
- `model llama2` - Switch to different model
- `quit` - Exit the application

## 🎯 Example Sessions

**System Administration:**
```
> memory usage
Code to execute: vm_stat
Execute this? [Y/n]: y
=== Bash Output ===
Pages free:                   123456.
Pages active:                 234567.
...
```

**File Management:**
```
> show me all log files larger than 1MB
Code to execute: find . -name "*.log" -size +1M -ls
Execute this? [Y/n]: y
=== Bash Output ===
drwxr-xr-x    1 user  staff   2048 Dec 19 10:30 ./app.log
...
```

## Accessibility
- The CLI uses colorized output for clarity, but all prompts are also readable as plain text.
- All commands are available via keyboard navigation.
- No mouse interaction is required.

## 📋 Requirements

- **Python 3.7+**
- **Local Ollama server** running with at least one model installed
  - Install Ollama: [https://ollama.com](https://ollama.com)
  - Recommended model: `ollama pull gemma3:4b`
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
```

## 🛠 Development

### Development Installation
```bash
git clone https://github.com/lukeslp/llamaline.git
cd llamaline
pip install -e .
```

### Project Structure
```
llamaline/
├── llamaline/
│   ├── __init__.py
│   └── llamaline.py      # Main CLI module
├── setup.py              # Package configuration
├── requirements.txt      # Dependencies
├── PROJECT_PLAN.md       # Roadmap and architecture
└── README.md            # This file
```

### Contributing
- See `PROJECT_PLAN.md` for roadmap and contribution guidelines
- Follow accessibility best practices
- Include tests for new features
- Update documentation as needed

## 🔒 Safety & Security

llamaline includes several safety features:
- **Command confirmation** before execution
- **Unsafe operation blocking** (prevents `sudo`, `rm -rf`, etc.)
- **Temporary file execution** for Python code
- **No persistent state** between commands

## 🌟 Community & Support

Having fun with **llamaline**? We'd love to hear from you!

| Connect With Us | Link |
|-----------------|------|
| 🐛 Issues & Features | [GitHub Issues](https://github.com/lukeslp/llamaline/issues) |
| 🛠️ Source Code | [GitHub Repository](https://github.com/lukeslp/llamaline) |
| 📧 Email | <luke@lukesteuber.com> |
| 🐦 Bluesky | [@lukesteuber.com](https://bsky.app/profile/lukesteuber.com) |
| 💼 LinkedIn | [lukesteuber](https://www.linkedin.com/in/lukesteuber/) |
| ✉️ Newsletter | [Substack](https://lukesteuber.substack.com/) |
| ☕ Support | [Tip Jar](https://usefulai.lemonsqueezy.com/buy/bf6ce1bd-85f5-4a09-ba10-191a670f74af) |

## 📄 License

Licensed under the **MIT License** by Luke Steuber. See [LICENSE](LICENSE) for details.

---

**Made with ❤️ for the accessibility community**
