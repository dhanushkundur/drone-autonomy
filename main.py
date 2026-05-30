from drone import connect, arm, takeoff, fly_to, return_to_launch

connection = connect()
arm(connection)
takeoff(connection, 15)

# Mission waypoints
fly_to(connection, -35.362261, 149.165230, 15)  # north
fly_to(connection, -35.362261, 149.166230, 15)  # northeast
fly_to(connection, -35.363261, 149.166230, 15)  # east
fly_to(connection, -35.363261, 149.165230, 15)  # back near home

return_to_launch(connection)