#Connect to the MAVLink device using pymavlink
from pymavlink import mavutil
import time
connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')
print("Waiting for heartbeat...")
connection.wait_heartbeat()
print("Heartbeat received")
print(f"Connected to system {connection.target_system}, component {connection.target_component}")

connection.set_mode('GUIDED')
print("Mode set to GUIDED")

print("Arming the vehicle...")
connection.arducopter_arm()
connection.motors_armed_wait()
print(f"Armed state: {connection.motors_armed() != 0}")
print("Vehicle armed")

print("Take off to 10 meters...")
connection.mav.command_long_send(
    connection.target_system,
    connection.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0,
    0, 0, 0, 0,
    0, 0,10
)
time.sleep(10)
msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
print(f"Current altitude: {msg.relative_alt/1000} m")
print("Should be at altitude 10 meters now")