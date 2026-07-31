from djitellopy import Tello
import time

drone = Tello()
drone.connect()
print(f"Battery: {drone.get_battery()}%")

# takeoff and go up 10ft
drone.takeoff()
time.sleep(1)
drone.move_up(457)
time.sleep(1)

'''
# 4 keys
drone.move_forward(100)
time.sleep(2)

drone.move_back(100)
time.sleep(2)

drone.move_left(100)
time.sleep(2)

drone.move_right(100)
time.sleep(2)
'''

# 5 keys
drone.move_forward(50)
time.sleep(1)

drone.move_back(50)
time.sleep(1)

drone.move_left(50)
time.sleep(1)

drone.move_right(50)
time.sleep(1)

drone.flip_forward()
time.sleep(1)

# land
drone.land()