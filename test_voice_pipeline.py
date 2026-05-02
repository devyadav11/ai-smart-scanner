import os
import sys
from unittest.mock import patch, MagicMock

# Mocking the tools that require physical hardware/Termux-API
with patch('os.system') as mock_os_system, \
     patch('subprocess.check_output') as mock_subprocess:
    
    # Mock voice input: "scan document"
    mock_subprocess.return_value = b"scan document"
    
    # Create a dummy image for the scanner to "find"
    dummy_img = "/storage/emulated/0/Download/photo_test.jpg"
    os.makedirs(os.path.dirname(dummy_img), exist_ok=True)
    from PIL import Image, ImageDraw
    img = Image.new('RGB', (100, 100), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10,10), "VOICE TEST SCAN", fill=(0,0,0))
    img.save(dummy_img)
    
    # Mock take_photo to return our dummy image
    # We need to mock it in main.py's namespace
    import main
    main.take_photo = MagicMock(return_value=dummy_img)
    
    print("--- RUNNING VOICE TEST ---")
    # Passing empty string triggers the voice listen() function
    main.agent("")
    print("--- TEST COMPLETE ---")

# Cleanup dummy files
if os.path.exists("smart_agent/output/scanned_doc.pdf"):
    print("SUCCESS: PDF was created.")
else:
    print("FAILED: PDF was not created.")
