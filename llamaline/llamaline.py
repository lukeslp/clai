#!/usr/bin/env python3
"""
ollama_tool_user.py

A CLI tool that uses a local Ollama model (gemma3:4b) to interpret natural-language prompts,
select between Python and shell execution tools, generate the needed code/command,
and execute it securely in a restricted environment.
"""
import os
import sys
import json
import ast
import asyncio
import tempfile
import requests
from typing import Generator, Optional, Dict

import argparse
import colorama
from colorama import Fore, Style

# Rich imports for styled CLI output
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

# Initialize colorama for ANSI styling
colorama.init(autoreset=True)

# Instantiate a Rich console for styled output
console = Console()

# -----------------------------------------------------------------------------
# Configuration (override via environment variables)
DEFAULT_ENDPOINT = os.environ.get('OLLAMA_ENDPOINT', 'http://localhost:11434')
DEFAULT_MODEL    = os.environ.get('OLLAMA_MODEL',  'gemma3:4b')

# -----------------------------------------------------------------------------
# Cheat-sheet shortcuts for common tasks
# -----------------------------------------------------------------------------
CHEAT_SHEETS: Dict[str, Dict[str, str]] = {
    "disk usage":         {"tool": "bash",   "code": "df -h"},
    "list files":         {"tool": "bash",   "code": "ls -al"},
    "memory usage":       {"tool": "bash",   "code": "vm_stat"},
    "running processes":  {"tool": "bash",   "code": "ps aux"},
    "network ports":      {"tool": "bash",   "code": "lsof -i -P -n | grep LISTEN"},
    "current directory":  {"tool": "bash",   "code": "pwd"},
    "say hello":          {"tool": "python", "code": "print('Hello, world!')"},
}
# -----------------------------------------------------------------------------

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
            # Pretty-print dict or JSON output (e.g., os.environ)
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
    # Using configurable endpoint
    ENDPOINT = DEFAULT_ENDPOINT

    def __init__(self, model: Optional[str] = None, endpoint: Optional[str] = None):
        # Allow overrides from args or env vars
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
# Main CLI
# -----------------------------------------------------------------------------
def main():
    # Parse command-line overrides
    parser = argparse.ArgumentParser(description="Natural-language to code executor")
    parser.add_argument("-m", "--model",    help="Ollama model to use",    default=None)
    parser.add_argument("-e", "--endpoint", help="Ollama API endpoint",    default=None)
    parser.add_argument("prompt", nargs=argparse.REMAINDER, help="Natural-language prompt to execute")
    args = parser.parse_args()

    # Instantiate with optional overrides via flags or env vars
    chat  = OllamaChat(model=args.model, endpoint=args.endpoint)
    tools = Tools()

    console.print(Panel(
        f"Model: [bold yellow]{chat.model}[/bold yellow]   Endpoint: [bold yellow]{chat.endpoint}[/bold yellow]\n"
        f"Commands: [bold]help[/bold] [bold]cheats[/bold] [bold]quit[/bold] [bold]model <name>[/bold]",
        border_style="cyan"
    ))

    # If prompt provided as CLI args, run once and exit
    if args.prompt:
        prompt = " ".join(args.prompt).strip()
        if not prompt:
            console.print("[red]No prompt provided.[/red]")
            return
        # Handle cheat-sheet
        key = prompt.lower()
        if key in CHEAT_SHEETS:
            choice = CHEAT_SHEETS[key]
        elif key in ("cheats", "help cheats", "list cheats"):
            console.print("[yellow]Available cheat-sheet commands:[/yellow]")
            for name in CHEAT_SHEETS:
                console.print(f"  - {name}")
            return
        else:
            console.print("[cyan]\n[↪] Analyzing and generating code...\n[/cyan]")
            try:
                choice = chat.select_tool(prompt)
            except Exception as e:
                console.print(f"[red]Error selecting tool: {e}[/red]")
                return
        tool = choice.get("tool")
        code = choice.get("code", "")
        console.print(f"[blue]Code to execute:[/blue]\n{code}")
        # Confirmation
        confirm = Prompt.ask("Execute this? (Y/n)", default="Y")
        if confirm.lower() not in ("y", "yes", ""):
            console.print("[red]Aborted.[/red]")
            return
        # Execute
        if tool == "bash":
            console.print(f"[blue]$ {code}[/blue]")
            result = asyncio.run(tools.run_bash_command(code))
            console.print("[green]\n=== Bash Output ===\n[/green]")
            console.print(result)
        elif tool == "python":
            console.print(f"[blue]```python\n{code}\n```\n[/blue]")
            result = asyncio.run(tools.run_python_code(code))
            console.print("[green]\n=== Python Output ===\n[/green]")
            console.print(result)
        else:
            console.print(f"[red]Unknown tool: {tool}[/red]")
        return

    try:
        while True:
            prompt = input(Fore.MAGENTA + "\nEnter your task (or 'quit' to exit):\n> " + Style.RESET_ALL).strip()
            if prompt.lower() in ('quit', 'exit'):
                break

            # Rich-styled built-in commands
            if prompt.lower() in ("help", "?"):
                console.print(Panel.fit(
                    "[bold cyan]Available commands[/bold cyan]\n"
                    "- [bold]help[/bold]: Show this help message\n"
                    "- [bold]cheats[/bold]: List cheat-sheet commands\n"
                    "- [bold]model[/bold]: Show current model\n"
                    "- [bold]model <name>[/bold]: Change to a different Ollama model\n"
                    "- [bold]quit[/bold]: Exit CLI",
                    title="Help", border_style="green"
                ))
                continue

            if prompt.lower().startswith("model"):
                parts = prompt.split(maxsplit=1)
                if len(parts) == 1:
                    console.print(f"[yellow]Current model:[/yellow] [bold]{chat.model}[/bold]")
                else:
                    new_model = parts[1].strip()
                    chat.model = new_model
                    console.print(f"[green]Model changed to:[/green] [bold]{chat.model}[/bold]")
                continue

            # Show and run cheat-sheet commands
            key = prompt.lower()
            if key in CHEAT_SHEETS:
                choice = CHEAT_SHEETS[key]
            elif key in ("cheats", "help cheats", "list cheats"):
                console.print("[yellow]Available cheat-sheet commands:[/yellow]")
                for name in CHEAT_SHEETS:
                    console.print(f"  - {name}")
                continue
            else:
                console.print("[cyan]\n[↪] Analyzing and generating code...\n[/cyan]")
                try:
                    choice = chat.select_tool(prompt)
                except Exception as e:
                    console.print(f"[red]Error selecting tool: {e}[/red]")
                    continue

            tool = choice.get('tool')
            code = choice.get('code', '')
            # Confirmation before execution
            console.print(f"[blue]\n[Preview] {tool} code:\n[/blue]{code}\n")
            confirm = input(Fore.YELLOW + "Execute this? [Y/n]: " + Style.RESET_ALL).strip().lower()
            if confirm not in ("y", "yes", ""):
                console.print("[red]Aborted.[/red]")
                continue

            if tool == 'bash':
                console.print(f"[blue]$ {code}[/blue]\n")
                result = asyncio.run(tools.run_bash_command(code))
                console.print("[green]\n=== Bash Output ===\n[/green]")
                console.print(result)

            elif tool == 'python':
                console.print(f"[blue]```python\n{code}\n```\n[/blue]")
                result = asyncio.run(tools.run_python_code(code))
                console.print("[green]\n=== Python Output ===\n[/green]")
                console.print(result)

            else:
                console.print(f"[red]Unknown tool: {tool}[/red]")

    except KeyboardInterrupt:
        console.print("\n[bold]Exiting...[/bold]")

if __name__ == '__main__':
    main()
