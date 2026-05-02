import os
import subprocess
import time
from rich.console import Console

console = Console()

def speak(text, rate=0.8, pause=1.0):
    """
    Convert text to speech using termux-tts-speak.
    rate: 1.0 is normal, lower is slower.
    pause: seconds to wait after speaking.
    """
    console.print(f"[italic cyan]AI Says: {text}[/italic cyan]")
    # Use -r flag to slow down speech
    os.system(f"termux-tts-speak -r {rate} \"{text}\"")
    # Add a small pause to give user time to react
    time.sleep(pause)

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
