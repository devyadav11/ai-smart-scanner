try:
    import cv2
    import numpy as np
    HAS_CV2 = True
except ImportError:
    from PIL import Image, ImageOps, ImageFilter
    HAS_CV2 = False

def enhance_image(input_path, output_path="smart_agent/output/enhanced.jpg"):
    if HAS_CV2:
        img = cv2.imread(input_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5,5), 0)
        thresh = cv2.adaptiveThreshold(
            blur, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY, 11, 2
        )
        cv2.imwrite(output_path, thresh)
    else:
        # Fallback using Pillow
        img = Image.open(input_path)
        gray = ImageOps.grayscale(img)
        # Apply a simple threshold for a "scanner" effect
        # First, enhance contrast
        enhanced = ImageOps.autocontrast(gray)
        # Simple binary threshold
        thresh = enhanced.point(lambda p: 255 if p > 128 else 0, mode='1')
        thresh.save(output_path)
        
    return output_path
