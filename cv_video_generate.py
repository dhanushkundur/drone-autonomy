import cv2
import numpy as np

# Video settings
width, height = 500, 500
fps = 30
duration_seconds = 5
total_frames = fps * duration_seconds

# Create a video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('test_video.mp4', fourcc, fps, (width, height))

# Generate frames with a moving red circle
for i in range(total_frames):
    # White background
    frame = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Circle moves from left to right across the frame
    progress = i / total_frames
    cx = int(50 + progress * (width - 100))
    cy = height // 2
    
    cv2.circle(frame, (cx, cy), 30, (0, 0, 255), -1)
    out.write(frame)

out.release()
print("Test video created: test_video.mp4")