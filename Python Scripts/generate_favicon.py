import os
import shutil
from PIL import Image

def generate_favicons():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    source_img_path = os.path.join(base_dir, "Image and Audio", "peacock-feather.png")
    
    if not os.path.exists(source_img_path):
        raise FileNotFoundError(f"Source icon not found at: {source_img_path}")
    
    src = Image.open(source_img_path).convert("RGBA")
    bbox = src.getbbox()
    cropped = src.crop(bbox)
    
    # Make a square canvas with subtle margin to prevent clipping on small browser tabs
    max_dim = max(cropped.width, cropped.height)
    pad_dim = int(max_dim * 1.1)
    square = Image.new("RGBA", (pad_dim, pad_dim), (0, 0, 0, 0))
    offset_x = (pad_dim - cropped.width) // 2
    offset_y = (pad_dim - cropped.height) // 2
    square.paste(cropped, (offset_x, offset_y), cropped)
    
    # Multi-resolution ICO sizes for crisp rendering across all displays and OS taskbars
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    
    # Root favicon.ico for standard browser GET /favicon.ico fallback
    root_ico_path = os.path.join(base_dir, "favicon.ico")
    square.save(root_ico_path, format="ICO", sizes=icon_sizes)
    
    # Image and Audio/ assets
    img_dir = os.path.join(base_dir, "Image and Audio")
    os.makedirs(img_dir, exist_ok=True)
    
    square.save(os.path.join(img_dir, "favicon.ico"), format="ICO", sizes=icon_sizes)
    square.resize((32, 32), Image.Resampling.LANCZOS).save(os.path.join(img_dir, "favicon-32x32.png"), format="PNG")
    square.resize((16, 16), Image.Resampling.LANCZOS).save(os.path.join(img_dir, "favicon-16x16.png"), format="PNG")
    square.resize((180, 180), Image.Resampling.LANCZOS).save(os.path.join(img_dir, "apple-touch-icon.png"), format="PNG")
    
    print("All favicon formats (root and Image and Audio/) generated successfully.")

if __name__ == "__main__":
    generate_favicons()
