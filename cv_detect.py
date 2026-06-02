import cv2
import numpy as np

# Load the test image
image = cv2.imread('test_image.jpg')

# Convert to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

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
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    center_x = x + w // 2
    center_y = y + h // 2
    
    # Print info
    print(f"Found object at ({x}, {y}) with size {w}x{h}")
    print(f"Center: ({center_x}, {center_y})")
else:
    print("No red object detected")

# Save the result
cv2.imwrite('output.jpg', image)
