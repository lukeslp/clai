#!/usr/bin/env python3
"""
llamaline.py

File Purpose: Main CLI module for the llamaline package - a natural-language to shell/Python assistant
Primary Functions/Classes: 
  - Tools: Executor class for Python and bash commands
  - OllamaChat: Interface for interacting with local Ollama models
  - main(): CLI entry point with rich interactive loop and narrow terminal support
Inputs and Outputs (I/O):
  - Input: Natural language prompts from user (supports narrow terminals)
  - Output: Executed code results with responsive Rich console output

A CLI tool that uses a local Ollama model (gemma3:4b) to interpret natural-language prompts,
select between Python and shell execution tools, generate the needed code/command,
and execute it securely in a restricted environment. Optimized for narrow terminals
with comprehensive Rich styling for enhanced interactivity.
"""
import os
import sys
import json
import ast
import asyncio
import tempfile
import requests
import textwrap
from typing import Generator, Optional, Dict, List
from datetime import datetime

import argparse

# Rich imports for comprehensive styled CLI output
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text
from rich.layout import Layout
from rich.columns import Columns
from rich.align import Align
from rich.rule import Rule
from rich import box
from rich.live import Live
from rich.spinner import Spinner
from rich.style import Style
from rich.theme import Theme

# Custom theme for consistent styling
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "prompt": "bold magenta",
    "code": "bold blue",
    "dim": "dim white",
})

# Instantiate a Rich console for styled output with custom theme
console = Console(theme=custom_theme)

# -----------------------------------------------------------------------------
# Configuration (override via environment variables)
DEFAULT_ENDPOINT = os.environ.get('OLLAMA_ENDPOINT', 'http://localhost:11434')
DEFAULT_MODEL    = os.environ.get('OLLAMA_MODEL',  'gemma3:4b')

# -----------------------------------------------------------------------------
# Cheat-sheet shortcuts for common tasks
# -----------------------------------------------------------------------------
CHEAT_SHEETS: Dict[str, Dict[str, str]] = {
    "disk usage":         {"tool": "bash",   "code": "df -h", "desc": "Show disk space usage"},
    "list files":         {"tool": "bash",   "code": "ls -al", "desc": "List all files with details"},
    "memory usage":       {"tool": "bash",   "code": "vm_stat", "desc": "Show memory statistics"},
    "running processes":  {"tool": "bash",   "code": "ps aux", "desc": "List all running processes"},
    "network ports":      {"tool": "bash",   "code": "lsof -i -P -n | grep LISTEN", "desc": "Show listening network ports"},
    "current directory":  {"tool": "bash",   "code": "pwd", "desc": "Print working directory"},
    "say hello":          {"tool": "python", "code": "print('Hello, world!')", "desc": "Simple Python greeting"},
}

# -----------------------------------------------------------------------------
# Utility Functions for Narrow Terminal Support
# -----------------------------------------------------------------------------
def get_terminal_width() -> int:
    """Get the current terminal width for responsive design"""
    return console.width

def wrap_text(text: str, width: Optional[int] = None) -> str:
    """Wrap text to fit terminal width"""
    if width is None:
        width = get_terminal_width() - 4  # Account for panel borders
    return "\n".join(textwrap.wrap(text, width=width))

def create_responsive_panel(content: str, title: str = "", border_style: str = "cyan", 
                          width_fraction: float = 1.0) -> Panel:
    """Create a panel that adapts to terminal width"""
    terminal_width = get_terminal_width()
    panel_width = min(int(terminal_width * width_fraction), terminal_width - 2)
    
    # Wrap content to fit panel
    wrapped_content = wrap_text(content, panel_width - 4)
    
    return Panel(
        wrapped_content,
        title=title,
        border_style=border_style,
        width=panel_width,
        expand=False
    )

def show_splash_screen():
    """Display an animated splash screen"""
    splash_text = """
    ╦  ╦  ╔═╗╔╦╗╔═╗╦  ╦╔╗╔╔═╗
    ║  ║  ╠═╣║║║╠═╣║  ║║║║║╣ 
    ╩═╝╩═╝╩ ╩╩ ╩╩ ╩╩═╝╩╝╚╝╚═╝
    """
    
    # Responsive splash for narrow terminals
    if get_terminal_width() < 50:
        splash_text = "LLAMALINE"
    
    console.print(
        Align.center(
            Text(splash_text, style="bold cyan"),
            vertical="middle"
        ),
        height=5
    )
    console.print(Align.center("[dim]Natural Language → Code[/dim]"))

# -----------------------------------------------------------------------------
# Executor Tools
# -----------------------------------------------------------------------------
class Tools:
    def __init__(self):
        self.python_path = sys.executable
        self.temp_dir = tempfile.gettempdir()

    async def run_python_code(self, code: str) -> str:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_path = f.name

            proc = await asyncio.create_subprocess_exec(
                self.python_path,
                temp_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.getcwd(),
                env=os.environ.copy()
            )
            stdout, stderr = await proc.communicate()
            os.unlink(temp_path)

            out = stdout.decode().strip()
            err = stderr.decode().strip()
            
            # Pretty-print dict or JSON output
            if not err:
                try:
                    val = ast.literal_eval(out)
                    if isinstance(val, dict):
                        out = json.dumps(val, indent=2, sort_keys=True)
                except Exception:
                    pass
            
            if err:
                return f"Error:\n{err}"
            return out or "No output"

        except Exception as e:
            return f"Error running Python code: {e}"

    async def run_bash_command(self, command: str) -> str:
        try:
            unsafe = ['sudo', 'rm -rf', '>', '>>', '|', '&', ';']
            if any(tok in command for tok in unsafe):
                return "Error: Command contains unsafe operations"

            proc = await asyncio.create_subprocess_exec(
                'sh', '-c', command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.getcwd(),
                env=os.environ.copy()
            )
            stdout, stderr = await proc.communicate()

            out = stdout.decode().strip()
            err = stderr.decode().strip()
            if err:
                return f"Error:\n{err}"
            return out or "No output"

        except Exception as e:
            return f"Error running bash command: {e}"

# -----------------------------------------------------------------------------
# OllamaChat for tool selection and code generation
# -----------------------------------------------------------------------------
class OllamaChat:
    def __init__(self, model: Optional[str] = None, endpoint: Optional[str] = None):
        self.endpoint = endpoint or os.environ.get('OLLAMA_ENDPOINT') or DEFAULT_ENDPOINT
        self.model    = model    or os.environ.get('OLLAMA_MODEL')    or DEFAULT_MODEL

    def select_tool(self, user_prompt: str) -> Dict[str, str]:
        # Build single-turn prompt for classification
        system = (
            "You are an assistant that takes a single natural-language prompt. "
            "Decide whether to use a shell command or a Python snippet to fulfill it. "
            "Respond with a raw JSON object with exactly two keys: "
            "\"tool\" (\"bash\" or \"python\") and \"code\" (the command or code snippet). "
            "Do NOT wrap the JSON in markdown or code fences. "
            "In the JSON, represent newlines in \"code\" using literal \"\\n\" characters, and do not include any literal line breaks. "
            "Do not include any additional text, comments, or formatting."
        )
        prompt_text = f"{system}\nUser: {user_prompt}\nAssistant:"
        
        # Send to Ollama single-turn generate endpoint
        url = f"{self.endpoint}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt_text,
            "stream": False
        }
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        
        # Extract single-turn response
        content = data.get("response", "")
        
        # Remove markdown fences if present
        import re
        m = re.search(r"```json\s*(?P<json>{.*?})\s*```", content, flags=re.S)
        json_str = m.group("json") if m else content.strip()
        
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            raw = resp.text
            raise ValueError(f"Invalid JSON from model: {raw}")

# -----------------------------------------------------------------------------
# UI Components for Rich Interactivity
# -----------------------------------------------------------------------------
def show_cheat_sheet():
    """Display cheat sheet in a responsive table"""
    table = Table(
        title="📋 Cheat Sheet Commands",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
        width=min(80, get_terminal_width() - 2)
    )
    
    # Adjust columns based on terminal width
    if get_terminal_width() > 60:
        table.add_column("Command", style="yellow", no_wrap=True)
        table.add_column("Type", style="cyan")
        table.add_column("Code", style="green")
        table.add_column("Description", style="dim")
        
        for name, info in CHEAT_SHEETS.items():
            table.add_row(
                name,
                f"[{info['tool']}]",
                info['code'][:30] + "..." if len(info['code']) > 30 else info['code'],
                info.get('desc', '')
            )
    else:
        # Narrow terminal: simplified view
        table.add_column("Command", style="yellow")
        table.add_column("Description", style="dim")
        
        for name, info in CHEAT_SHEETS.items():
            table.add_row(name, info.get('desc', info['tool']))
    
    console.print(table)

def show_help():
    """Display help information with responsive layout"""
    help_items = [
        ("help", "Show this help message"),
        ("cheats", "List available shortcuts"),
        ("model", "Show current model"),
        ("model <name>", "Change Ollama model"),
        ("history", "Show command history"),
        ("clear", "Clear the screen"),
        ("quit", "Exit the application"),
    ]
    
    if get_terminal_width() > 50:
        # Wide terminal: two-column layout
        table = Table(box=None, show_header=False, padding=(0, 2))
        table.add_column("Command", style="bold cyan")
        table.add_column("Description")
        
        for cmd, desc in help_items:
            table.add_row(f"[bold]{cmd}[/bold]", desc)
        
        console.print(Panel(table, title="🔧 Available Commands", border_style="green"))
    else:
        # Narrow terminal: vertical list
        content = "\n".join([f"• [bold cyan]{cmd}[/bold cyan]\n  {desc}" for cmd, desc in help_items])
        console.print(create_responsive_panel(content, title="🔧 Commands", border_style="green"))

def display_code_preview(tool: str, code: str) -> None:
    """Display code with syntax highlighting and responsive wrapping"""
    terminal_width = get_terminal_width()
    
    # Create syntax-highlighted code
    if tool == "python":
        syntax = Syntax(code, "python", theme="monokai", word_wrap=True, 
                       line_numbers=terminal_width > 60)
    else:
        syntax = Syntax(code, "bash", theme="monokai", word_wrap=True,
                       line_numbers=terminal_width > 60)
    
    # Responsive panel title
    title = f"💻 {tool.title()} Code Preview"
    if terminal_width < 40:
        title = f"{tool.title()}"
    
    panel = Panel(
        syntax,
        title=title,
        border_style="blue",
        width=min(terminal_width - 2, 100),
        expand=False
    )
    console.print(panel)

def display_result(tool: str, result: str) -> None:
    """Display command results with responsive formatting"""
    # Truncate very long results for narrow terminals
    max_lines = 20 if get_terminal_width() < 50 else 50
    lines = result.split('\n')
    
    if len(lines) > max_lines:
        result = '\n'.join(lines[:max_lines])
        result += f"\n\n[dim]... ({len(lines) - max_lines} more lines)[/dim]"
    
    # Create output panel
    if "Error" in result:
        panel_style = "red"
        title = "❌ Error Output"
    else:
        panel_style = "green"
        title = f"✅ {tool.title()} Output"
    
    if get_terminal_width() < 40:
        title = "Output"
    
    console.print(create_responsive_panel(result, title=title, border_style=panel_style))

def show_startup_menu(model: str, endpoint: str):
    """Display startup menu with responsive design"""
    terminal_width = get_terminal_width()
    
    # Show splash screen only on wide terminals
    if terminal_width > 50:
        show_splash_screen()
        console.print()
    
    # Model and endpoint info
    info_text = f"Model: [bold yellow]{model}[/bold yellow]"
    if terminal_width > 60:
        info_text += f"   Endpoint: [bold yellow]{endpoint}[/bold yellow]"
    
    # Quick commands
    if terminal_width > 40:
        commands = "Commands: [bold]help[/bold] • [bold]cheats[/bold] • [bold]model[/bold] • [bold]quit[/bold]"
    else:
        commands = "Type [bold]help[/bold] for commands"
    
    content = f"{info_text}\n{commands}"
    
    console.print(create_responsive_panel(
        content,
        title="🚀 Llamaline CLI" if terminal_width > 30 else "Llamaline",
        border_style="cyan"
    ))

# -----------------------------------------------------------------------------
# Main CLI with Enhanced Interactivity
# -----------------------------------------------------------------------------
async def process_prompt(prompt: str, chat: OllamaChat, tools: Tools) -> None:
    """Process a single prompt with rich feedback"""
    # Check for cheat sheet command
    key = prompt.lower()
    if key in CHEAT_SHEETS:
        choice = CHEAT_SHEETS[key]
        console.print(f"\n[dim]Using cheat sheet: {key}[/dim]")
    else:
        # Generate code with progress indicator
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Analyzing prompt and generating code...", total=None)
            
            try:
                choice = chat.select_tool(prompt)
                progress.update(task, completed=True)
            except Exception as e:
                progress.update(task, completed=True)
                console.print(Panel(
                    f"Failed to generate code: {str(e)}",
                    title="❌ Error",
                    border_style="red"
                ))
                return

    tool = choice.get("tool")
    code = choice.get("code", "")
    
    # Display code preview
    console.print()
    display_code_preview(tool, code)
    
    # Confirmation with Rich prompt
    console.print()
    if not Confirm.ask("[prompt]Execute this code?[/prompt]", default=True):
        console.print("[warning]⚠️  Execution cancelled[/warning]")
        return
    
    # Execute with progress indicator
    console.print()
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
        console=console
    ) as progress:
        task = progress.add_task(f"[cyan]Running {tool} code...", total=None)
        
        if tool == "bash":
            result = await tools.run_bash_command(code)
        elif tool == "python":
            result = await tools.run_python_code(code)
        else:
            result = f"Unknown tool: {tool}"
        
        progress.update(task, completed=True)
    
    # Display results
    console.print()
    display_result(tool, result)

def main():
    # Parse command-line overrides
    parser = argparse.ArgumentParser(description="Natural-language to code executor")
    parser.add_argument("-m", "--model",    help="Ollama model to use",    default=None)
    parser.add_argument("-e", "--endpoint", help="Ollama API endpoint",    default=None)
    parser.add_argument("prompt", nargs=argparse.REMAINDER, help="Natural-language prompt to execute")
    args = parser.parse_args()

    # Instantiate with optional overrides
    chat  = OllamaChat(model=args.model, endpoint=args.endpoint)
    tools = Tools()

    # Show startup menu
    show_startup_menu(chat.model, chat.endpoint)

    # If prompt provided as CLI args, run once and exit
    if args.prompt:
        prompt = " ".join(args.prompt).strip()
        if not prompt:
            console.print("[error]No prompt provided.[/error]")
            return
        
        # Handle special commands
        if prompt.lower() in ("cheats", "help cheats", "list cheats"):
            show_cheat_sheet()
            return
        
        # Process the prompt
        asyncio.run(process_prompt(prompt, chat, tools))
        return

    # Interactive loop with command history
    command_history: List[str] = []
    
    try:
        while True:
            console.print()
            
            # Responsive prompt
            if get_terminal_width() > 50:
                prompt_text = "[prompt]Enter your task (or 'quit' to exit):[/prompt]"
            else:
                prompt_text = "[prompt]Task:[/prompt]"
            
            prompt = Prompt.ask(prompt_text, console=console)
            prompt = prompt.strip()
            
            if prompt.lower() in ('quit', 'exit', 'q'):
                break

            # Handle built-in commands
            if prompt.lower() in ("help", "?", "h"):
                show_help()
                continue

            if prompt.lower() == "clear":
                console.clear()
                show_startup_menu(chat.model, chat.endpoint)
                continue

            if prompt.lower() == "history":
                if command_history:
                    history_panel = create_responsive_panel(
                        "\n".join([f"{i+1}. {cmd}" for i, cmd in enumerate(command_history[-10:])]),
                        title="📜 Recent Commands",
                        border_style="blue"
                    )
                    console.print(history_panel)
                else:
                    console.print("[dim]No command history yet[/dim]")
                continue

            if prompt.lower().startswith("model"):
                parts = prompt.split(maxsplit=1)
                if len(parts) == 1:
                    console.print(f"[info]Current model:[/info] [bold]{chat.model}[/bold]")
                else:
                    new_model = parts[1].strip()
                    chat.model = new_model
                    console.print(f"[success]✓ Model changed to:[/success] [bold]{chat.model}[/bold]")
                continue

            if prompt.lower() in ("cheats", "help cheats", "list cheats", "shortcuts"):
                show_cheat_sheet()
                continue

            # Add to history and process
            command_history.append(prompt)
            asyncio.run(process_prompt(prompt, chat, tools))

    except KeyboardInterrupt:
        console.print("\n[warning]⚡ Interrupted by user[/warning]")
    except Exception as e:
        console.print(f"\n[error]Unexpected error: {e}[/error]")
    finally:
        # Farewell message
        console.print("\n[dim]Thanks for using Llamaline! 👋[/dim]")

if __name__ == '__main__':
    main()
