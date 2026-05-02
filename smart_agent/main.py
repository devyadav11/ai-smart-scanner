import sys
import os
from tools.camera import take_photo
from tools.enhance import enhance_image
from tools.pdf import image_to_pdf
from tools.ocr import extract_text
from tools.voice import speak, listen
from rich.console import Console

console = Console()

def scan_document():
    speak("Starting scan. Please hold the document steady.")
    console.print("[bold blue]📸 Taking photo...[/bold blue]")
    img = take_photo()
    
    if not os.path.exists(img) or os.path.getsize(img) == 0:
        speak("Error. I couldn't capture the photo.")
        console.print("[bold red]Error: Photo not saved or is empty. Make sure Termux-API is working and camera permissions are granted.[/bold red]")
        return

    speak("Processing image.")
    console.print("[bold blue]🧹 Enhancing...[/bold blue]")
    enhanced = enhance_image(img, "smart_agent/output/enhanced.jpg")

    console.print("[bold blue]📄 Creating PDF...[/bold blue]")
    pdf = image_to_pdf(enhanced, "smart_agent/output/scanned_doc.pdf")

    console.print("[bold blue]🔍 Extracting text (OCR)...[/bold blue]")
    text = extract_text(enhanced)
    
    speak("Scan complete. PDF is ready.")
    console.print(f"[bold green]✅ Done![/bold green]")
    console.print(f"PDF saved to: [cyan]{pdf}[/cyan]")
    
    if text.strip():
        console.print("[bold yellow]OCR Preview:[/bold yellow]")
        console.print(text[:200] + ("..." if len(text) > 200 else ""))
    else:
        console.print("[yellow]No text detected.[/yellow]")

def agent(prompt):
    if not prompt:
        speak("I am listening. What should I do?")
        prompt = listen()

    prompt = prompt.lower()
    if "scan" in prompt:
        scan_document()
    elif "listen" in prompt or "voice" in prompt:
        speak("Voice mode activated. What can I do for you?")
        new_prompt = listen()
        agent(new_prompt)
    else:
        speak("Unknown command. I can scan documents if you ask.")
        console.print(f"[red]Unknown command:[/red] {prompt}")
        console.print("Try: [green]scan document[/green] or [green]voice[/green]")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        agent(prompt)
    else:
        console.print("[bold yellow]Smart Agent CLI[/bold yellow]")
        console.print("Usage: python main.py \"scan document\"")
