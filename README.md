# 📱 AI Smart Scanner (Termux + Gemini)

An autonomous, voice-controlled, and web-enabled document scanner built entirely on Android using Termux. This project uses Gemini AI for intelligent document processing and Tesseract for OCR.

## 🌟 Features

- **🚀 Autonomous Pipeline:** Automatically enhances images, converts them to PDF, and extracts text (OCR).
- **🎙️ Voice Interaction:** "Hey AI, scan this!" - Fully voice-controlled using Termux-API with natural timing.
- **🌐 Web App & PWA:** Modern web interface to bypass hardware limitations, installable as a native app on your home screen.
- **📁 Smart Storage:** Automatically saves unique, timestamped PDFs to a dedicated `scanned document` folder inside your phone's **Documents** folder.
- **🔒 100% Local:** No API keys required. All processing (OCR, Enhancement, PDF) happens entirely on your phone.

## 🛠️ Tech Stack

- **Backend:** Python (FastAPI, Uvicorn)
- **AI/OCR:** Google Gemini SDK, Tesseract OCR
- **Image Processing:** OpenCV (with Pillow fallbacks)
- **Frontend:** HTML5, Tailwind CSS, JavaScript (PWA)
- **Environment:** Termux (Android)

## 🚀 Quick Start

### 1. Prerequisites
Install the required packages in Termux:
```bash
pkg update && pkg upgrade
pkg install python tesseract termux-api
pip install fastapi uvicorn pillow pytesseract rich google-genai
```

### 2. Run the App
To start the voice-controlled CLI:
```bash
ai voice
```
To start the Web/PWA App:
```bash
scanner-app
```
Then open `http://localhost:5000` in your browser.

## 📂 Project Structure
- `smart_agent/tools/`: Core logic for camera, voice, PDF, and OCR.
- `smart_agent/static/`: PWA frontend and manifest.
- `smart_agent/web_app.py`: FastAPI backend.
- `main.py`: CLI Orchestrator.

## ⚖️ License
MIT
<!-- Automated Sync Active -->
