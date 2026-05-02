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
PUBLIC_BASE_DIR = "/storage/emulated/0/Documents/scanned document"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(PUBLIC_BASE_DIR, exist_ok=True)

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
        speak("I have received your document. Enhancing it now.")
        
        enhanced_path = os.path.join(OUTPUT_DIR, "enhanced.jpg")
        enhance_image(input_path, enhanced_path)
        
        temp_pdf_path = os.path.join(OUTPUT_DIR, "temp_scan.pdf")
        image_to_pdf(enhanced_path, temp_pdf_path)
        
        # 3. Local Organization (Timestamp based)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        final_filename = f"Scan_{timestamp}.pdf"
        public_pdf_path = os.path.join(PUBLIC_BASE_DIR, final_filename)
        
        shutil.copy(temp_pdf_path, public_pdf_path)
        
        text = extract_text(enhanced_path)
        speak("Scan complete. I have saved the PDF to your scanned document folder.")
        
        return {
            "success": True, 
            "filename": final_filename,
            "ocr_preview": text[:100],
            "message": f"Saved as {final_filename}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
