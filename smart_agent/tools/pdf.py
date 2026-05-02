from PIL import Image
import os

def image_to_pdf(image_path, pdf_path="smart_agent/output/output.pdf"):
    # Ensure output directory exists if provided
    dir_name = os.path.dirname(pdf_path)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
    
    img = Image.open(image_path).convert("RGB")
    img.save(pdf_path)
    return pdf_path
