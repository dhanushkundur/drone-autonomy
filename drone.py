from pymavlink import mavutil
import time
import math

def connect(address='udp:127.0.0.1:14550'):
    connection = mavutil.mavlink_connection(address)
    print("Waiting for heartbeat...")
    connection.wait_heartbeat()
    print("Heartbeat received")
    print(f"Connected to system {connection.target_system}, component {connection.target_component}")
    return connection

def arm(connection):
    connection.set_mode('GUIDED')
    print("Mode set to GUIDED")
    print("Arming the vehicle...")
    connection.arducopter_arm()
    connection.motors_armed_wait()
    print(f"Armed state: {connection.motors_armed() != 0}")
    print("Vehicle armed")

def takeoff(connection, altitude):
    print(f"Take off to {altitude} meters...")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
        0,
        0, 0, 0, 0,
        0, 0, altitude
    )
    while True:
        msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            current_altitude = msg.relative_alt / 1000
            print(f"Current altitude: {current_altitude} m")
            if current_altitude >= altitude * 0.95: 
                print("Reached target altitude")
                break
        time.sleep(1)

def fly_to(connection, latitude, longitude, altitude):
    print(f"Flying to ({latitude}, {longitude}) at {altitude}m...")
    connection.mav.set_position_target_global_int_send(
        0,
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,
        0b0000111111111000,
        int(latitude * 10**7),
        int(longitude * 10**7),
        altitude,
        0, 0, 0,
        0, 0, 0,
        0, 0
    )
    while True:
        msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        if msg:
            current_lat = msg.lat / 10**7
            current_lon = msg.lon / 10**7
            distance = distance_meters(current_lat, current_lon, latitude, longitude)
            print(f"Distance to target: {distance:.1f} m")
            if distance < 1:
                print("Arrived")
                break
        time.sleep(1)

def distance_meters(lat1, lon1, lat2, lon2):
    lat_diff_m = (lat2 - lat1) * 111_320
    lon_diff_m = (lon2 - lon1) * 111_320 * math.cos(math.radians(lat1))
    return math.sqrt(lat_diff_m**2 + lon_diff_m**2)