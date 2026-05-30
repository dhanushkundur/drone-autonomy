from drone import connect, arm, takeoff, fly_to, land

connection = connect()
arm(connection)
takeoff(connection, 10)
fly_to(connection, -35.362261, 149.165230, 10)
land(connection)