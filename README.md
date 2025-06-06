---
**llamaline**  
MIT License  
Author: Luke Steuber  
Web: [actuallyusefulai.com](https://actuallyusefulai.com), [lukesteuber.com](https://lukesteuber.com)
---

# llamaline

A natural-language to shell/Python CLI assistant using local Ollama models.

## Installation

```bash
pip install .
```

Or, for development:

```bash
pip install -e .
```

## Usage

After installation, use the `llamaline` command:

```bash
llamaline "Show me disk usage"
```

Or start the interactive CLI:

```bash
llamaline
```

## Accessibility
- The CLI uses colorized output for clarity, but all prompts are also readable as plain text.
- All commands are available via keyboard navigation.
- No mouse interaction is required.

## Requirements
- Python 3.7+
- Local Ollama server running (see project plan for details)

## Development
- See `PROJECT_PLAN.md` for roadmap and contribution guidelines. 