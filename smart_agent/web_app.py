from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import shutil
import os
from tools.enhance import enhance_image
from tools.pdf import image_to_pdf
from tools.ocr import extract_text
from tools.voice import speak

app = FastAPI()

# Create necessary directories
UPLOAD_DIR = "smart_agent/uploads"
OUTPUT_DIR = "smart_agent/output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="smart_agent/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("smart_agent/static/index.html") as f:
        return f.read()

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 1. Save uploaded file
        input_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 2. Pipeline: Enhance -> PDF -> OCR
        speak("Processing scan from web app.")
        
        enhanced_path = os.path.join(OUTPUT_DIR, "enhanced.jpg")
        enhance_image(input_path, enhanced_path)
        
        pdf_path = os.path.join(OUTPUT_DIR, "web_scan.pdf")
        image_to_pdf(enhanced_path, pdf_path)
        
        # 3. Move to Public 'scanned document' Folder
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        public_dir = "/storage/emulated/0/scanned document"
        
        try:
            if not os.path.exists(public_dir):
                os.makedirs(public_dir, exist_ok=True)
                print(f"Created public directory: {public_dir}")
            
            public_pdf_path = os.path.join(public_dir, f"Scan_{timestamp}.pdf")
            shutil.copy(pdf_path, public_pdf_path)
            print(f"Copied to public storage: {public_pdf_path}")
            display_msg = f"Saved to: scanned document/Scan_{timestamp}.pdf"
        except Exception as e:
            print(f"Public storage copy failed: {e}")
            display_msg = "Document processed (Local Only)"

        text = extract_text(enhanced_path)
        
        speak("Scan complete. Your PDF is ready.")
        
        return {
            "success": True, 
            "pdf": pdf_path, 
            "ocr_preview": text[:100],
            "message": display_msg
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
