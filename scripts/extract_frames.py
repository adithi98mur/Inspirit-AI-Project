import cv2
import os
from google.colab import drive
from concurrent.futures import ThreadPoolExecutor

# Mount Drive
drive.mount('/content/drive')

# Paths
video_file = "/content/drive/MyDrive/IMG_1853.mov"  # your video in Drive root
output_dir = "/content/drive/MyDrive/frames"        # frames saved into Drive

# Create the output folder if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

def save_frame(frame, filepath):
    """Function to save a single frame to disk."""
    cv2.imwrite(filepath, frame)
    print(f"✅ Saved: {os.path.basename(filepath)}")

def extract_frames(video_path, output_folder, max_workers=4):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ Error: Cannot open video file: {video_path}")
        return

    frame_number = 0
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        while True:
            ret, frame = cap.read()
            if not ret:
                break  # End of video

            filename = f"frame_{frame_number:04d}.png"
            filepath = os.path.join(output_folder, filename)

            # Submit save task to thread pool
            executor.submit(save_frame, frame.copy(), filepath)

            frame_number += 1

    cap.release()
    print("🎉 Done! All frames extraction tasks submitted.")

# Run the extraction
extract_frames(video_file, output_dir, max_workers=16)
