import cv2
import os
from google.colab import drive

# Mount Drive
drive.mount('/content/drive')

# Paths
video_file = "/content/drive/MyDrive/IMG_1853.mov"  # your video in Drive root
output_dir = "/content/drive/MyDrive/frames"        # frames saved into Drive

def extract_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"❌ Error: Cannot open video file: {video_path}")
        return

    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # End of video

        filename = f"frame_{frame_number:04d}.png"
        filepath = os.path.join(output_folder, filename)
        cv2.imwrite(filepath, frame)
        print(f"✅ Saved: {filename}")
        frame_number += 1

    cap.release()
    print("🎉 Done! All frames extracted.")

# Call function only once
extract_frames(video_file, output_dir)
