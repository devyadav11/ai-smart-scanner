import os
import subprocess
from rich.console import Console

console = Console()

def speak(text):
    """Convert text to speech using termux-tts-speak."""
    console.print(f"[italic cyan]AI Says: {text}[/italic cyan]")
    os.system(f"termux-tts-speak \"{text}\"")

def listen():
    """Listen for voice input using termux-speech-to-text."""
    console.print("[bold green]👂 Listening...[/bold green]")
    try:
        # Run termux-speech-to-text and capture output
        result = subprocess.check_output(["termux-speech-to-text"], stderr=subprocess.STDOUT)
        text = result.decode("utf-8").strip()
        console.print(f"[bold white]You said: {text}[/bold white]")
        return text
    except Exception as e:
        console.print(f"[bold red]Speech recognition error: {e}[/bold red]")
        return ""
