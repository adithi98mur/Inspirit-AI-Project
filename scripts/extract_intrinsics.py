import cv2
import numpy as np
import glob
import os
from google.colab import drive

# --- MOUNT DRIVE ---
drive.mount('/content/drive')

# --- SETTINGS ---
video_file = "/content/drive/MyDrive/IMG_1859.MOV"  # Path to your checkerboard video
frames_dir = "/content/frames"                      # Temp folder for extracted frames
checkerboard_size = (9, 6)  # Inner corners (columns, rows) — adjust to your board

# --- STEP 1: Extract frames from video ---
os.makedirs(frames_dir, exist_ok=True)
cap = cv2.VideoCapture(video_file)
frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if frame_count % 10 == 0:  # Save 1 every 10 frames
        cv2.imwrite(f"{frames_dir}/frame_{frame_count:04d}.png", frame)
    frame_count += 1
cap.release()
print(f"✅ Extracted {len(os.listdir(frames_dir))} frames")

# --- STEP 2: Prepare object points ---
# 3D points in real-world space (Z=0)
objp = np.zeros((checkerboard_size[1]*checkerboard_size[0], 3), np.float32)
objp[:, :2] = np.mgrid[0:checkerboard_size[0], 0:checkerboard_size[1]].T.reshape(-1, 2)

objpoints = []  # 3D points
imgpoints = []  # 2D points

# --- STEP 3: Find corners in each frame ---
images = glob.glob(f"{frames_dir}/*.png")
for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, checkerboard_size, None)
    if ret:
        objpoints.append(objp)
        imgpoints.append(corners)
        # Draw corners for visual check
        cv2.drawChessboardCorners(img, checkerboard_size, corners, ret)
        cv2.imwrite(fname.replace(".png", "_corners.png"), img)

print(f"✅ Found corners in {len(imgpoints)} / {len(images)} frames")

# --- STEP 4: Calibrate camera ---
if len(objpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, gray.shape[::-1], None, None
    )

    print("\n🎯 CAMERA CALIBRATION RESULTS")
    print("Intrinsic Matrix (K):\n", mtx)
    print("\nDistortion Coefficients:\n", dist.ravel())

    # Save calibration
    np.savez("/content/drive/MyDrive/calibration_data.npz",
             intrinsic_matrix=mtx,
             distortion_coeffs=dist,
             rotation_vectors=rvecs,
             translation_vectors=tvecs)
    print("\n💾 Calibration saved to Drive: calibration_data.npz")
else:
    print("❌ No corners detected. Check your checkerboard size or video quality.")
