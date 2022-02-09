import setup_path
import airsim
import numpy as np
from threading import Thread
import time
from navigator import orbit
import math

# ip = "192.168.0.11"
# client = airsim.MultirotorClient(ip=ip)
# lidar_client = airsim.MultirotorClient(ip=ip)

client = airsim.MultirotorClient()
lidar_client = airsim.MultirotorClient()

filename = ""
record_data = False

def lidar_execute():
    print('Scanning Has Started\n')
    print('Use Keyboard Interrupt \'CTRL + C\' to Stop Scanning\n')
    existing_data_cleared = False   #change to true to superimpose new scans onto existing .asc files
    try:
        while record_data:
            
            file_name_with_ext = f"{filename}.asc"
            if not existing_data_cleared:
                f = open(file_name_with_ext,'w')
            else:
                f = open(file_name_with_ext,'a')
            lidar_data =lidar_client.getLidarData(vehicle_name='Drone1',lidar_name='LidarSensor2')
                    
            orientation = lidar_data.pose.orientation
            q0, q1, q2, q3 = orientation.w_val, orientation.x_val, orientation.y_val, orientation.z_val
            rotation_matrix = np.array(([1-2*(q2*q2+q3*q3),2*(q1*q2-q3*q0),2*(q1*q3+q2*q0)],
                                        [2*(q1*q2+q3*q0),1-2*(q1*q1+q3*q3),2*(q2*q3-q1*q0)],
                                        [2*(q1*q3-q2*q0),2*(q2*q3+q1*q0),1-2*(q1*q1+q2*q2)]))

            position = lidar_data.pose.position
            for i in range(0, len(lidar_data.point_cloud), 3):
                xyz = lidar_data.point_cloud[i:i+3]

                corrected_x, corrected_y, corrected_z = np.matmul(rotation_matrix, np.asarray(xyz))
                final_x = corrected_x + position.x_val
                final_y = corrected_y + position.y_val
                final_z = corrected_z + position.z_val

                f.write("%f %f %f\n" % (final_x,final_y,final_z))
            f.close()
            time.sleep(0.2)
            existing_data_cleared = True
    except KeyboardInterrupt:
        airsim.wait_key('Press any key to stop running this script')
        print("Done!\n")
    
    finally:
        return

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
    filename = "ıcp_foto"
    #TODO: dronu yukseltecek kod yazilacak
    #TODO: dron donerken veri toplanip gorsellestirilecek
    #TODO: lidar veri miktari azaltilacak ve deneme yapilacak

    lidarThread = Thread(target=lidar_execute,daemon=True)
    
    client.confirmConnection()
    #lidar_execute.confirmConnection()
    client.enableApiControl(False)
    client.enableApiControl(True)
    client.armDisarm(False)
    
    #airsim.wait_key('Kalkis icin bir tusa basiniz')
    client.armDisarm(True)
    client.takeoffAsync().join()

    #airsim.wait_key('Yukselis icin bir tusa basiniz')
    client.moveToZAsync(-16, 5).join()
    #client.moveByVelocityZAsync(0,0, -5 ,0.20, airsim.DrivetrainType.MaxDegreeOfFreedom, airsim.YawMode(False, 53)).join()
    #Gamepadim yanimda olmadigindan elimle yon vermek icin yazdim usttekini xdd
    
    client.hoverAsync().join()

    #airsim.wait_key('Veri toplama ve yorunge icin bir tusa basiniz')
    record_data = True
    
    drone_posistion = client.getMultirotorState().kinematics_estimated.position
    current_altitude = drone_posistion.z_val
    
    orientation = client.getMultirotorState().kinematics_estimated.orientation
        
    
    #ACI HESAPLARI BASLANGIC :
    #convert quaternion to euler
    roll_x, pitch_y, yaw_z = euler_from_quaternion(orientation.x_val, orientation.y_val, orientation.z_val, orientation.w_val)
    
    yaw_z = yaw_to_degrees(yaw_z)
    print(roll_x, pitch_y, yaw_z)

    point_a = orientation.x_val + 10*math.cos(yaw_z*math.pi/180)
    point_b = orientation.y_val + 10*math.sin(yaw_z*math.pi/180)

    print(point_a, point_b)

    center_vector = [point_a-orientation.x_val,point_b-orientation.y_val]
    print(center_vector)

    #ACI HESAPLARI BITIS
    w_val = orientation.w_val
    
    orbit_radius = 27

    nav = orbit.OrbitNavigator(client =client,radius=orbit_radius,altitude=current_altitude, speed=2, iterations=1, center = center_vector, snapshots=0)
    lidarThread.start()
    nav.start_orbit()

    #airsim.wait_key("inis yapmak icin bir tusa basiniz")
    record_data = False
    client.moveToZAsync(-1, 5).join()
    
    client.landAsync().join()
    #client.armDisarm(False)
    
    client.enableApiControl(False)

    pass