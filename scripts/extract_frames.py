import cv2
import os

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

        # Save each frame as a PNG
        filename = f"frame_{frame_number:04d}.png"
        filepath = os.path.join(output_folder, filename)
        cv2.imwrite(filepath, frame)
        print(f"✅ Saved: {filename}")
        frame_number += 1

    cap.release()
    print("🎉 Done! All frames extracted.")

# Example usage
if __name__ == "__main__":
    video_file = "your_video.mov"     # Replace with your iPhone video filename
    output_dir = "frames"             # Folder to save frames

    extract_frames(video_file, output_dir)
