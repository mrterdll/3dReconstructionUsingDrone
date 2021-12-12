import airsim
from airsim import client,Quaternionr
import time
import math
from pyquaternion import Quaternion as quat



if __name__ == "__main__":
    ip = "192.168.0.11"
 
    #client = airsim.MultirotorClient(ip=ip) 
    client = airsim.MultirotorClient() 

    action_quat = quat([6,0,0,0])



    typeDrivetrain = airsim.DrivetrainType.MaxDegreeOfFreedom
    # Movement forward with velocity 6 in the x direction
    #action = [6, 0, 0]
    # Get current motorstate and transform them to quaternion
    q             = client.simGetVehiclePose().orientation 
    my_quaternion = Quaternionr(w_val = q.w_val,
                            x_val = q.x_val,
                            y_val = q.y_val,
                            z_val = q.z_val)
    mvm           = my_quaternion.rotate(action_quat)
    velocities = client.getMultirotorState().kinematics_estimated.angular_velocity
    donre_vel_rota =[velocities.x_val , velocities.y_val]
    # Perform the movement
    client.moveByVelocityZAsync(vx = donre_vel_rota[0] + mvm[0],
                vy          = donre_vel_rota[1] + mvm[1],
                z           = -1.8,
                duration    = 0.2, 
                drivetrain  = typeDrivetrain,
                yaw_mode    = airsim.YawMode(is_rate = True,  
                                            yaw_or_rate = 0))

"""
    while True:

        altitude = client.getMultirotorState().kinematics_estimated.position.z_val
       # print(altitude)

        orientation = client.getMultirotorState().kinematics_estimated.orientation.w_val
        sin = math.sin(orientation)
        cos = math.cos(orientation)
        print(sin,cos)        

        #rc_data = client.getMultirotorState().rc_data.yaw
        #print(rc_data)

        time.sleep(2)
"""