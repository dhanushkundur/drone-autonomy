from drone import Drone

drone = Drone()
drone.connect()
drone.arm()
drone.takeoff(10)
drone.fly_to(-35.362261, 149.165230, 10)
drone.return_to_launch()