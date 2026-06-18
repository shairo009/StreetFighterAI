"""Create GIF from frames"""
import os
from PIL import Image

frames_dir = "frames"
output = "AI_Fight.gif"

frame_files = sorted([f for f in os.listdir(frames_dir) if f.endswith('.png')])

if not frame_files:
    print("No frames found!")
    exit(1)

print(f"Creating GIF from {len(frame_files)} frames...")

images = [Image.open(os.path.join(frames_dir, f)) for f in frame_files]
images[0].save(output, save_all=True, append_images=images[1:], duration=125, loop=0)

print(f"✅ GIF saved: {output}")
