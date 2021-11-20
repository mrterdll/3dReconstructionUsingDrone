import airsim
from airsim import client
import time






if __name__ == "__main__":
    ip = "192.168.0.11"
 
    #client = airsim.MultirotorClient(ip=ip) 
    client = airsim.MultirotorClient() 

    while True:

        altitude = client.getMultirotorState().kinematics_estimated.position.z_val
        print(altitude)

        orientation = client.getMultirotorState().kinematics_estimated.orientation
        print(orientation)

        time.sleep(2)