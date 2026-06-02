import cv2
import numpy as np

cap = cv2.VideoCapture('test_video.mp4')

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break  # video ended
    
    # YOUR DETECTION CODE GOES HERE
    # Same logic as cv_detect.py but operating on `frame` instead of `image`
    # Print the center if found
    # Load the test image

# Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red range in HSV
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])

    # Create a mask: white pixels where red is, black elsewhere
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours (outlines of white blobs in the mask)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # If we found at least one contour
    if len(contours) > 0:
        # Get the biggest contour by area
        biggest = max(contours, key=cv2.contourArea)
        
        # Get its bounding box
        x, y, w, h = cv2.boundingRect(biggest)
        
        # Draw a green rectangle on the original image
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Print info
        print(f"Found object at ({x}, {y}) with size {w}x{h}")
        print(f"Center: ({center_x}, {center_y})")
    else:
        print("No red object detected")

    # Save the result

    
    frame_count += 1

cap.release()
print(f"Processed {frame_count} frames")