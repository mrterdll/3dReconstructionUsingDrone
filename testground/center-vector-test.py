import airsim
from airsim import client,Quaternionr
import time
import math

 
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians


#convert yaw to degrees
def yaw_to_degrees(yaw):
    return math.degrees(yaw)



if __name__ == "__main__":
    ip = "192.168.0.11"
 
    #client = airsim.MultirotorClient(ip=ip) 
    client = airsim.MultirotorClient() 
    client.enableApiControl(True)
    degree = 0

    while True:

        altitude = client.getMultirotorState().kinematics_estimated.position.z_val
       # print(altitude)

        orientation = client.getMultirotorState().kinematics_estimated.orientation

        #convert quaternion to euler
        roll_x, pitch_y, yaw_z = euler_from_quaternion(orientation.x_val, orientation.y_val, orientation.z_val, orientation.w_val)
        
        

        #convert -3 - 3 to 0 - 360
        #yaw_z = yaw_z * 180 / math.pi
        yaw_z = yaw_to_degrees(yaw_z)
        print(roll_x, pitch_y, yaw_z)
        #client.moveToPositionAsync( orientation.x_val,orientation.y_val,7, 2).join()

        

        point_a = orientation.x_val + 10*math.cos(yaw_z*math.pi/180)
        point_b = orientation.y_val + 10*math.sin(yaw_z*math.pi/180)

        print(point_a, point_b)

        direction_vector = [point_a-orientation.x_val,point_b-orientation.y_val]
        print(direction_vector)
        

        client.moveByVelocityZAsync(0,0, -7 ,0.20, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, degree)).join()
        degree = degree+1
        #time.sleep(0.20)
