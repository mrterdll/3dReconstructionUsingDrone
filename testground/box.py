import setup_path
import airsim

import sys
import time

from math import *
import numpy

client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)
client.armDisarm(True)
client.takeoffAsync().join()

print("Flying a small square box using moveByVelocityZ")

# AirSim uses NED coordinates so negative axis is up.
# z of -15 is 15 meters above the original launch point.
z = -15

# Fly given velocity vector for 6 seconds
duration = 6
speed = 1
delay = speed * duration

radius = 6
temp1 = (1/2) * radius
temp3 = (round(sqrt(3), 2)/2) * radius

# using airsim.DrivetrainType.MaxDegreeOfFreedom means we can control the drone yaw independently
# from the direction the drone is flying.  I've set values here that make the drone always point inwards
# towards the inside of the box (which would be handy if you are building a 3d scan of an object in the real world).
vy = 0
vx = -radius
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=0")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 0)).join()
time.sleep(delay)

vy = -temp1 - vy
vx = -temp3 - vx
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=30")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 30)).join()
time.sleep(delay)

vy = -temp3 - (-temp1)
vx = -temp1 - (-temp3)
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=60")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 60)).join()
time.sleep(delay)

vy = -radius - (-temp3)
vx = temp1
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=90")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 90)).join()
time.sleep(delay)

vy = -temp3 - (-radius)
vx = temp1
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=120")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 120)).join()
time.sleep(delay)

vy = -temp1 - (-temp3)
vx = temp3 - temp1
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=150")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 150)).join()
time.sleep(delay)

vy = temp1
vx = radius - temp3
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=180")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 180)).join()
time.sleep(delay)

vy = temp1
vx = temp3 - radius
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=210")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 210)).join()
time.sleep(delay)

vy = temp3 - temp1
vx = temp1 - temp3
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=240")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 240)).join()
time.sleep(delay)

vy = radius - temp3
vx = -temp1
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=270")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 270)).join()
time.sleep(delay)

vy = temp3 - radius
vx = -temp1
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=300")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 300)).join()
time.sleep(delay)

vy = temp1 - temp3
vx = -temp3 - (-temp1)
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=330")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 330)).join()
time.sleep(delay)

vy = -temp1
vx = -radius - (-temp3)
print("moving by velocity vx=" + str(vx) + ", vy=" + str(vy) + ", yaw=360")
client.moveByVelocityZAsync(vx,vy,z,duration, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 360)).join()
time.sleep(delay)

# Ending position
client.moveToPositionAsync( 0, 0, -15, 3).join()
client.moveToPositionAsync( 0, 0, 0, 3).join()

client.hoverAsync().join()
client.landAsync().join()