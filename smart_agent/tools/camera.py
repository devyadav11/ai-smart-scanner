import os
from datetime import datetime

def take_photo(camera_id="0"):
    # Ensure the directory exists
    save_dir = "/storage/emulated/0/Download"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        
    filename = f"{save_dir}/photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    # Use -c flag to specify camera ID
    cmd = f"termux-camera-photo -c {camera_id} {filename}"
    print(f"Executing: {cmd}")
    os.system(cmd)
    return filename
