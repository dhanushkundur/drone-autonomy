#Connect to the MAVLink device using pymavlink
from pymavlink import mavutil
connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')
print("Waiting for heartbeat...")
connection.wait_heartbeat()
print("Heartbeat received")
print(f"Connected to system {connection.target_system}, component {connection.target_component}")

msg = connection.recv_match(type='SYS_STATUS', blocking=True)
print(f"Battery Voltage: {msg.voltage_battery/1000} V")
