# 🦙 llamaline v1.0.0 - "The Llama Has Landed!"

**Transform your terminal into a natural language powerhouse!** 🚀

Ever wished you could just *tell* your computer what to do in plain English? Now you can! llamaline bridges the gap between human thoughts and machine commands, making the command line accessible to everyone.

## 🎉 What is llamaline?

Think of it as your friendly neighborhood llama that translates your wishes into code:
- 💬 **"Show me disk usage"** → Runs `df -h`
- 🐍 **"Calculate fibonacci numbers"** → Generates and runs Python code
- 🔍 **"Find large log files"** → Executes the perfect bash command

All powered by your local Ollama models - no cloud, no API keys, just you and your helpful llama! 🦙

## ✨ Key Features

- **🗣️ Natural Language Magic** - Type what you want in plain English
- **🛡️ Safety First** - Previews commands before running (no accidental `rm -rf /`)
- **⚡ Lightning Fast** - Built-in shortcuts for common tasks
- **🎨 Beautiful Output** - Rich, colorized terminal experience
- **♿ Accessibility Champion** - Full keyboard navigation, screen reader friendly
- **🔄 Model Flexibility** - Switch between Ollama models on the fly

## 🚀 Quick Start

```bash
# Install (30 seconds!)
pip install llamaline

# One-liner magic
llamaline "show me what's eating my disk space"

# Interactive mode
llamaline
> list all python files modified today
> what's using port 8080?
> make me a dad joke in python
```

## 📦 Installation Options

<details>
<summary><b>🐍 PyPI</b> (Recommended)</summary>

```bash
pip install llamaline
```
</details>

<details>
<summary><b>🔧 From Source</b></summary>

```bash
git clone https://github.com/lukeslp/llamaline.git
cd llamaline
pip install -e .
```
</details>

<details>
<summary><b>🐻 Conda</b> (Coming Soon!)</summary>

```bash
conda install -c conda-forge llamaline
```
</details>

## 🎯 Built-in Cheats

Just type these shortcuts:
- `disk usage` • `memory usage` • `running processes`
- `list files` • `network ports` • `say hello`

## 📋 Prerequisites

- **Python 3.7+** 🐍
- **[Ollama](https://ollama.com)** with a model (we recommend `gemma3:4b`)

## 🎪 See It In Action!

```
llamaline
╭─────────────────────────────────────────────────╮
│ Model: gemma3:4b   Endpoint: localhost:11434   │
│ Commands: help cheats quit model <name>         │
╰─────────────────────────────────────────────────╯

> find all TODO comments in my code

[Preview] bash code:
grep -r "TODO" --include="*.py" --include="*.js" .

Execute this? [Y/n]: y

=== Bash Output ===
./app.py:42:    # TODO: Add error handling
./utils.js:18:  // TODO: Optimize this function
...
```

## 🤝 Join the Herd!

Created with ❤️ by **[Luke Steuber](https://lukesteuber.com)** - Speech therapist turned code whisperer, making tech accessible one llama at a time!

| 🔗 Connect | 📍 Where |
|------------|----------|
| 💻 Code | [GitHub](https://github.com/lukeslp/llamaline) |
| 🐛 Issues | [Bug Reports](https://github.com/lukeslp/llamaline/issues) |
| 📧 Email | [luke@lukesteuber.com](mailto:luke@lukesteuber.com) |
| 🦋 Social | [Bluesky](https://bsky.app/profile/lukesteuber.com) • [LinkedIn](https://linkedin.com/in/lukesteuber) |
| 📰 Updates | [Newsletter](https://lukesteuber.substack.com/) |
| ☕ Support | [Buy me a coffee](https://usefulai.lemonsqueezy.com/buy/bf6ce1bd-85f5-4a09-ba10-191a670f74af) |

## 📜 License

MIT License - Use it, love it, share it! Just keep the attribution. 🙏

---

**🎊 Thank you for trying llamaline!** If it makes your life easier, give it a ⭐ and tell your friends!

*Special thanks to the Ollama team for making local LLMs accessible, and to the accessibility community for inspiring this project.*

> **Fun fact:** This release was tested by having a llama explain quantum physics using only food analogies. It worked! 🌮⚛️

#NaturalLanguageCLI #Accessibility #LocalLLMs #MadeWithLove 