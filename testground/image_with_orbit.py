from airsim.types import YawMode
import setup_path
import airsim
import numpy as np
from threading import Thread
import time
from navigator import orbit
import cv2
import os
import tempfile
import sys
import math

# ip = "192.168.0.11"
# client = airsim.MultirotorClient(ip=ip)
# lidar_client = airsim.MultirotorClient(ip=ip)

client = airsim.MultirotorClient()
camera_client = airsim.MultirotorClient()

filename = ""
record_data = False

def camera_execute():
    print('Scanning Has Started\n')
    print('Use Keyboard Interrupt \'CTRL + C\' to Stop Scanning\n')
    existing_data_cleared = False   #change to true to superimpose new scans onto existing .asc files
    try:
        fontFace = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        thickness = 2
        textSize, baseline = cv2.getTextSize("FPS", fontFace, fontScale, thickness)
        print(textSize)
        textOrg = (10, 10 + textSize[1])
        frameCount = 0
        startTime = time.time()
        fps = 0
        #filename = "ıcp_foto"
        count = 0
        while record_data:
            
            # because this method returns std::vector<uint8>, msgpack decides to encode it as a string unfortunately.
            rawImage = camera_client.simGetImage("high_res_45_degree", airsim.ImageType.Scene)
            if (rawImage == None):
                print("Camera is not returning image, please check airsim for error messages")
                sys.exit(0)
            else:
                png = cv2.imdecode(airsim.string_to_uint8_array(rawImage), cv2.IMREAD_UNCHANGED)
                cv2.putText(png,'FPS ' + str(fps),textOrg, fontFace, fontScale,(255,0,255),thickness)
                #cv2.imshow("Depth", png)
                #cv2.imshow("scene", png)
                
                airsim.write_file(os.path.normpath("./foto/"+filename+str(count)+ '.png'), airsim.string_to_uint8_array(rawImage))
                count+=1
            frameCount = frameCount  + 1
            endTime = time.time()
            diff = endTime - startTime
            if (diff > 1):
                fps = frameCount
                frameCount = 0
                startTime = endTime
            time.sleep(2)
            key = cv2.waitKey(1) & 0xFF
            if (key == 27 or key == ord('q') or key == ord('x')):
                break
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
    filename = "ıcp_foto_2mahalle"
    #TODO: dronu yukseltecek kod yazilacak
    #TODO: dron donerken veri toplanip gorsellestirilecek
    #TODO: lidar veri miktari azaltilacak ve deneme yapilacak

    cameraThread = Thread(target=camera_execute,daemon=True)
    
    client.confirmConnection()
    camera_client.confirmConnection()
    client.enableApiControl(False)
    client.enableApiControl(True)
    client.armDisarm(False)
    
    #airsim.wait_key('Kalkis icin bir tusa basiniz')
    client.armDisarm(True)
    client.takeoffAsync().join()


    #airsim.wait_key('Yukselis icin bir tusa basiniz')
    
    client.moveToZAsync(-35, 5).join()
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
    
    orbit_radius = 35


    nav = orbit.OrbitNavigator(client =client,radius=orbit_radius,altitude=current_altitude, speed=2, iterations=1, center = center_vector, snapshots=0)
    cameraThread.start()
    nav.start_orbit()

    #airsim.wait_key("inis yapmak icin bir tusa basiniz")
    record_data = False
    client.moveToZAsync(-1, 5).join()
    
    client.landAsync().join()
    #client.armDisarm(False)
    
    client.enableApiControl(False)

    pass