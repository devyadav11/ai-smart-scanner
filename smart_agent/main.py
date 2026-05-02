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
        console.print("[bold red]Error: Photo not saved or is empty.[/bold red]")
        return

    speak("Enhancing the image.")
    console.print("[bold blue]🧹 Enhancing...[/bold blue]")
    enhanced = enhance_image(img, "smart_agent/output/enhanced.jpg")

    temp_pdf = "smart_agent/output/temp_scan.pdf"
    image_to_pdf(enhanced, temp_pdf)

    # Organize in public storage (Timestamp based)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    public_dir = "/storage/emulated/0/Documents/scanned document"
    os.makedirs(public_dir, exist_ok=True)
    
    final_path = os.path.join(public_dir, f"Scan_{timestamp}.pdf")
    import shutil
    shutil.copy(temp_pdf, final_path)
    
    speak("Done. I have saved your document.")
    console.print(f"[bold green]✅ Saved to:[/bold green] {final_path}")
    
    text = extract_text(enhanced)
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
