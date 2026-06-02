import cv2
import numpy as np

# Create a 500x500 white image
image = np.ones((500, 500, 3), dtype=np.uint8) * 255

# Draw a red circle on it
# Note: OpenCV uses BGR not RGB, so red is (0, 0, 255)
cv2.circle(image, (250, 250), 50, (0, 0, 255), -1)

# Save it so we can look at it
cv2.imwrite('test_image.jpg', image)
print("Test image created")