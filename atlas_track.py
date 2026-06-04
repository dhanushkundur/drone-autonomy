import cv2
import numpy as np
import time
from pymavlink import mavutil
from drone import connect, arm, takeoff, land

# Constants
FRAME_WIDTH = 500
FRAME_CENTER_X = FRAME_WIDTH // 2
YAW_GAIN = 0.05  # how aggressively to react

def send_yaw_command(connection, yaw_change_degrees):
    """Send a relative yaw command to the drone."""
    direction = 1 if yaw_change_degrees > 0 else -1
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_CONDITION_YAW,
        0,
        abs(yaw_change_degrees),  # angle (always positive)
        20,                       # yaw rate (degrees/sec)
        direction,                # direction
        1,                        # relative (1 = relative to current)
        0, 0, 0
    )

# Connect and prep drone
connection = connect()
arm(connection)
takeoff(connection, 10)
print("Ready to track")

# Open video
cap = cv2.VideoCapture('test_video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # 2. Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # 3. If contour exists, get center
    if len(contours) > 0:
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        center_x = x + w // 2
        center_y = y + h // 2
        print(f"Found object at ({x}, {y}) with size {w}x{h}")
        print(f"Center: ({center_x}, {center_y})")
    else:
        print("No red object detected")
        continue  # skip to next frame if no object found
    # 4. Compute error_x = center_x - FRAME_CENTER_X
    error_x = center_x - FRAME_CENTER_X
    # 5. Compute yaw command: yaw_change = error_x * YAW_GAIN
    yaw_change = error_x * YAW_GAIN
    # 6. Send the yaw command using send_yaw_command()
    send_yaw_command(connection, yaw_change)
    # 7. Print error and yaw for debugging
    print(f"Error: {error_x}, Yaw: {yaw_change}")

    time.sleep(0.1)  # small delay so drone has time to react

cap.release()
print("Video ended")
land(connection)